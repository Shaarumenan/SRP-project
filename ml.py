from flask import Flask, request, render_template
app = Flask(__name__)
from flask_socketio import SocketIO
from pandas import DataFrame
import joblib
import pandas as pd
import numpy as np
import csv
from matplotlib import pyplot as plt
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
#socketio = SocketIO(app)

import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="SRP"
)
mycursor = mydb.cursor()
@app.route('/')
@app.route('/login')
def login():
    return render_template('sub.html')

def extractDigits(lst):
	return list(map(lambda el:[el], lst))

@app.route('/', methods=['POST'])
def my_form_post():
    if request.method == 'POST':
       id = request.form['id']
       #pid = request.form['pid']
       #print(id,pid)
       if id == []:
           return render_template('sub.html')
       else:
           idcheck = "SELECT rollno from marks WHERE rollno=%s" % id
           mycursor.execute(idcheck)
           idresult1 = mycursor.fetchall()
           #print(idresult1)
           if idresult1 == []:
               return render_template('sub.html')
           print(id)
           sql = "SELECT sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8 FROM marks WHERE rollno=%s" % id
           mycursor.execute(sql)
           mark = mycursor.fetchall()
           #print(type(mark))
           marklist = [item for t in mark for item in t]
           #print(marklist)
           marks = extractDigits(marklist)
           #print(marks)
           #af = DataFrame(marks(1,0), columns=['s1','s2','s3','s4','s5','s6','s7','s8'])
           #print(af)
           df = DataFrame(marks, columns=['marks'])
           #print(df)
           with open('C:\\Users\\mrsub\\Desktop\\inp.csv', 'w', newline='') as out_file:
               writer = csv.writer(out_file)
               writer.writerow(['s1','s2','s3','s4','s5','s6','s7','s8'])
               writer.writerow([marks[0][0],marks[1][0],marks[2][0],marks[3][0],marks[4][0],marks[5][0],marks[6][0],marks[7][0]])
           clf = joblib.load('domain.pkl')
           fname = pd.read_csv("C:\\Users\\mrsub\\Desktop\\inp.csv")
           print(fname)
           plt.plot(fname)
           plt.savefig('/static/images/new_plot.png')
           # predicting
           global op
           op = clf.predict(fname)
           print((op))
           print(op[0])
           if op[0] == 0:
               opsr='Hardware'
           elif op[0] == 1:
               opsr='Software'
           elif op[0] == 2:
               opsr ='Needs improvement in Both Hardware and Software domain'
           elif op[0] == 3:
               opsr ='Good in Both Software and Hardware domains'
           np.savetxt("C:\\Users\\mrsub\\Desktop\\outp.csv", op, delimiter=",")
           return render_template('login1.html',opp=opsr,)




if __name__ == '__main__':
    app.run()
    app.debug=True
mycursor.close()
mydb.close()