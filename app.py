import os
from flask import Flask,render_template,request,session
from flask_mail import Mail,Message
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = "hello"

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "example"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_UNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')



mail = Mail(app)
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.form['una']
        session["name"] = name
        des = request.form['de']
        cur = mysql.connection.cursor()
        cur.execute("select * from ex1 where name='"+name+"' and des='"+des+"'")
        r = cur.fetchall()
        if len(r)>0:
            return render_template("student.html",nametxt=name)
        else:
            return render_template("login.html")
    return render_template("login.html")	


@app.route('/faculty_login',methods=['GET','POST'])
def faculty_login():
    if request.method == 'POST':
       fname = request.form['fna']
       session["fname"] = fname
       fpwd = request.form['fpw']
       cur = mysql.connection.cursor()
       cur.execute("select * from ex3 where fname='"+fname+"' and fpass='"+fpwd+"'")
       r = cur.fetchall()
       if len(r)>0:
           return render_template("faculty.html",fnametxt=fname)
       else:
           return render_template("flogin.html")
    return render_template("flogin.html")


@app.route('/result')
def result():
    cur = mysql.connection.cursor()
    if "name" in session:
        user1 = session["name"]
        cur.execute("SELECT AVG(sub1),AVG(sub2),AVG(sub3),AVG(sub4),AVG(sub5),AVG(sub6),AVG(sub7),AVG(sub8)FROM marks")
        avg = cur.fetchone()
        res = cur.execute("SELECT * FROM marks where roll_no='"+user1+"'")
        if res > 0:
             result = cur.fetchone()
             return render_template('result.html',details=result,avg1=avg)
             cur.close()
    return f"<h1>{user1}</h1>"

@app.route('/doubt',methods =['GET','POST'])
def doubt():
    cur = mysql.connection.cursor()
    if "name" in session:
        user2 = session["name"]
        if request.method == 'POST':
            staff_ = request.form['stna']
            doubt_ = request.form['dou']
            cur = mysql.connection.cursor()
            cur.execute("insert into doubt (staff,details,student) VALUES (%s,%s,%s)", (staff_,doubt_,user2))
            mysql.connection.commit()
            return render_template('doubt2.html')
            cur.close()
        return render_template('doubt.html')

@app.route('/doubt_view')
def doubt_view(): 
    cur = mysql.connection.cursor()
    if "fname" in session:
        fac_name = session["fname"]
        cur.execute("SELECT details,student FROM doubt where staff='"+fac_name+"'")
        dou = cur.fetchall()
        if len(dou)>0:
            return render_template("doubt_view.html",fac_n=fac_name,dou=dou)
        else:
            return render_template("no_doubt.html",fac_n=fac_name)
        cur.close()

@app.route('/delete_doubt')
def delete_doubt():
    cur = mysql.connection.cursor()
    if "fname" in session:
        fac_name = session["fname"]
        cur.execute("DELETE FROM doubt where staff='"+fac_name+"'")
        mysql.connection.commit()
        return "DELETED"
        cur.close()




@app.route('/email',methods=['GET','POST'])
def email():
    if request.method== 'POST':
        rno = request.form['rno']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM email")
        eid = cur.fetchone()
        esid = str(eid)
        if len(eid)>0:
            message = Message('Example',sender="shaarumenan2000@gmail.com",recipients=[esid]) 
            message.body = f'''hello'''
		
            mail.send(message)
		
            return render_template("eres.html")
        else:
            return "Failed"

@app.route('/student')
def student():
    return render_template("student.html")

@app.route('/faculty')
def faculty():
    return render_template("faculty.html")
if __name__ == "__main__":
    app.run(debug=True)
	