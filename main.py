from typing import Any, Union

from flask import Flask,render_template,request,url_for,redirect,session
import time

from werkzeug.utils import secure_filename

from mylib import *
import os


app=Flask(__name__)

app.config['UPLOAD_FOLDER']='./static/photos'
app.secret_key="super secret key"

@app.route('/')
def welcome():
    return render_template('Welcome.html')


@app.route('/signup')
def signup():
    return render_template('SignUp.html')


@app.route('/adminreg',methods=['GET','POST'])
def adminreg():
    if 'usertype' in session:
        ut = session['usertype']
        e1=session['email']
        if ut == 'admin':
            if request.method=='POST':
                #collect form data and save it
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']
                email=request.form['T4']
                password=request.form['T5']
                usertype="admin"

                cur=userdb()

                sql="insert into admindata values('"+name+"','"+address+"','"+contact+"','"+email+"')"
                sql2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"

                cur.execute(sql)
                n=cur.rowcount

                cur.execute(sql2)
                m=cur.rowcount

                msg="Error: Cannot save data try again"
                if n==1 and m==1 :
                    msg='Data saved and login created'
                elif n==1:
                    msg='Data saved but login not created'
                elif m==1:
                    msg='Login created but data not saved'
                #send response
                return render_template('AdminRegistration.html',msg=msg)
            else:
                return render_template('AdminRegistration.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/student_reg',methods=['GET','POST'])
def student_reg():
    if request.method=='POST':
        #collect form data and save it
        name=request.form['T1']
        branch=request.form['T2']
        roll=request.form['T3']
        contact=request.form['T4']
        email=request.form['T5']
        password=request.form['T6']
        confirm=request.form['T7']
        #connectivity
        conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='studs',autocommit=True)
        cur=conn.cursor()

        sql="insert into studentdata values('"+name+"','"+branch+"','"+roll+"','"+contact+"','"+email+"')"
        sql2="insert into logindata values('"+email+"','"+password+"','student')"

        cur.execute(sql)
        n=cur.rowcount

        cur.execute(sql2)
        m=cur.rowcount

        msg="Error: Cannot save data try again"
        if n==1 and m==1 :
            msg='Data saved and login created'
        elif n==1:
            msg='Data saved but login not created'
        elif m==1:
            msg='Login created but data not saved'
        #send response
        return render_template('student_reg.html',kota=msg)
    else:
        return render_template('student_reg.html')

@app.route('/solve',methods=['GET','POST'])
def solve():
    if 'usertype' in session:
        ut = session['usertype']
        e1=session['email']
        if ut == 'student':

            if request.method=='POST':
                qid=request.form['qid']
                question=request.form['question']
                subject=request.form['subject']
                dt=request.form['date']
                data=(qid,question,subject,dt)
                solutions = getsolutions(qid)
                return render_template('solve.html', data1=data, solutions=solutions)
            else:
                sql = "select * from qbank where qby<> '" + e1 + "'  order by qid desc"
                cur = userdb()
                cur.execute(sql)
                n = cur.rowcount
                if n > 0:
                    obj = cur.fetchall()
                    return render_template('Solve.html', data=obj)
                else:
                    return render_template('Solve.html', msg="No question found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))



@app.route('/solve1',methods=['GET','POST'])
def solve1():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='student':
            if request.method=='POST':
                solution=request.form['T1']
                qid=request.form['qid']
                solby=e1
                soldate=str(int(time.time()))
                sql="insert into solutions(qid,solution,soldate,solby) values("+qid+",'"+solution+"',"+soldate+",'"+solby+"')"
                cur=userdb()
                cur.execute(sql)
                n=cur.rowcount
                msg="Error: Try again"
                if n==1:
                    msg="Solution Uploaded"
                return render_template('Solve1.html',msg=msg)
            else:
                return redirect(url_for('solve'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/logindata')
def logindata():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='studs', autocommit=True)
    cur = conn.cursor()
    sql = "select * from studentdata"

    cur.execute(sql)
    n = cur.rowcount
    if n>0:
        data=cur.fetchall()
        return render_template('logindata.html',jpr=data)
    else:
        msg="No data found"
        return render_template('logindata.html',kota=msg)

@app.route('/find_data',methods=['GET','POST'])
def find_data():
    if request.method=='POST':
        roll=request.form['T2']
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='studs', autocommit=True)
        cur = conn.cursor()
        sql = "select * from studentdata where roll='"+roll+"'"
        cur.execute(sql)
        n = cur.rowcount
        if(n==1):
            a=cur.fetchone()
            return render_template('showstudent.html',data=a)
        else:
            return render_template('showstudent.html', data1="No Data Found..!!")
    else:
        return render_template('showstudent.html')

@app.route('/findformdata',methods=['GET','POST'])
def findformdata():
    if request.method=='POST':
        roll=request.form['T3']
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='studs', autocommit=True)
        cur = conn.cursor()
        sql = "select * from studentdata where roll='"+roll+"'"
        cur.execute(sql)
        n = cur.rowcount
        if(n==1):
            a=cur.fetchone()
            return render_template('findformdata.html',data=a)
        else:
            return render_template('findformdata.html', data1="No Data Found..!!")
    else:
        return render_template('findformdata.html')


@app.route('/logout')
def logout():
    if 'usertype' in session:
        session.pop('usertype',None)
        session.pop('email',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/admin_home')
def admin_home():
    if 'usertype' in session:
        usertype=session['usertype']
        if usertype=='admin':
            return render_template('AdminHome.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/student_home')
def student_home():
    if 'usertype' in session:
        usertype=session['usertype']
        if usertype=='student':
            return render_template('StudentHome.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/auth_error')
def auth_error():
    return render_template('AuthError.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['T1']
        password=request.form['T2']
        cur=userdb()

        sql = "select * from logindata where email='"+email+"' and password='"+password+"'"

        cur.execute(sql)
        n = cur.rowcount
        if n==1:
            data=cur.fetchone()
            usertype=data[2]


            #session creating
            session["usertype"]=usertype
            session["email"]=email


            if usertype=='admin':
               return redirect(url_for('admin_home'))
            elif usertype=='student':
               return redirect(url_for('student_home'))
        else:
            return render_template('Login.html',msg="Incorrect email or password")
    else:
        return render_template('Login.html')

@app.route('/change_password_admin',methods=['GET','POST'])
def change_password_admin():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']

        if ut=='admin':
            if request.method=='POST':
                oldpass=request.form['T1']
                newpass=request.form['T2']
                conpass=request.form['T3']
                cur=userdb()


                   # msg='enter correct old password'

                   # return render_template('ChangePasswordAdmin.html', msg=msg)

                if oldpass==newpass:
                    if newpass==conpass:
                        msg='password same'
                        return render_template('ChangePasswordAdmin.html',msg=msg)
                    else:
                        msg='confirm password not match'
                        return render_template('ChangePasswordAdmin.html',msg=msg)

                else:
                        if newpass==None and conpass==None:
                            msg='Please Enter Something,The Password Cannot Be NULL'
                            return render_template('ChangePasswordAdmin.html',msg=msg)

                        if newpass!=None and conpass!=None:
                            msg='Wrong Password'
                            if newpass==conpass:
                                sql="update logindata set password='"+newpass+"' where email='"+e1+"' AND password='"+oldpass+"'"
                                cur.execute(sql)
                                n=cur.rowcount

                                if n==1:
                                    msg='password changed'
                            return render_template('ChangePasswordAdmin.html',msg=msg)


            else:
                return render_template('ChangePasswordAdmin.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))



@app.route('/change_password_student',methods=['GET','POST'])
def change_password_student():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']

        if ut=='student':
            if request.method=='POST':
                oldpass=request.form['T1']
                newpass=request.form['T2']
                conpass=request.form['T3']
                cur=userdb()


                   # msg='enter correct old password'

                   # return render_template('ChangePasswordAdmin.html', msg=msg)

                if oldpass==newpass:
                    if newpass==conpass:
                        msg='Password Same'
                        return render_template('ChangePasswordStudent.html',msg=msg)
                    else:
                        msg='Confirm Password Does Not Match'
                        return render_template('ChangePasswordStudent.html',msg=msg)

                else:
                        if newpass==None and conpass==None:
                            msg='Password Not Change'
                            return render_template('ChangePasswordStudent.html',msg=msg)

                        if newpass!=None and conpass!=None:
                            msg='Wrong Password'
                            if newpass==conpass:
                                sql="update logindata set password='"+newpass+"' where email='"+e1+"' AND password='"+oldpass+"'"
                                cur.execute(sql)
                                n=cur.rowcount

                                if n==1:
                                    msg='password changed'
                            return render_template('ChangePasswordStudent.html',msg=msg)
            else:
                return render_template('ChangePasswordStudent.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))



@app.route('/ask',methods=['GET','POST'])
def ask():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='student':
            if request.method=='POST':
                qsub=request.form['T1']
                question=request.form['T2']
                qby=e1
                qdate=int(time.time())
                sql="insert into qbank(qsub,question,qdate,qby) values('"+qsub+"','"+question+"',"+str(qdate)+",'"+qby+"')"
                cur=userdb()
                cur.execute(sql)
                n=cur.rowcount
                msg="Error: Try again"
                if n==1:
                    msg="Question uploaded"

                return render_template('Ask.html',msg=msg)
            else:
                return render_template('Ask.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))




@app.route('/show_admins')
def show_admins():
    cur=userdb()
    sql = "select * from admindata"

    cur.execute(sql)
    n = cur.rowcount
    if n>0:
        data=cur.fetchall()
        return render_template('Show_Admins.html',jpr=data)
    else:
        msg="No data found"
        return render_template('Show_Admins.html',kota=msg)




@app.route('/myquestions')
def myquestions():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='student':
            sql="select * from qbank where qby='"+e1+"'  order by qid desc"
            cur=userdb()
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                obj=cur.fetchall()
                return render_template('MyQuestions.html',data=obj)
            else:
                return render_template('MyQuestions.html',msg="No question found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/mysolutions',methods=['GET','POST'])
def mysolutions():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='student':
            sql="select * from solutions where solby='"+e1+"'  order by sid desc"
            cur=userdb()
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                obj=cur.fetchall()
                return render_template('MySolutions.html',data=obj)
            else:
                return render_template('MySolutions.html',msg="No question found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/solutions')
def solutions():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='student':
            sql="select * from qbank where qby='"+e1+"'  order by qid desc"
            cur=userdb()
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                obj=cur.fetchall()
                return render_template('Solutions.html',data=obj)
            else:
                return render_template('Solutions.html',msg="No solution found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/admin_profile',methods=['GET','POST'])
def admin_profile():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='admin':
            if request.method=='POST':
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']
                photo=checkphoto(e1)
                cur=userdb()
                sql="update admindata set name='"+name+"',address='"+address+"',contact='"+contact+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    image = checkphoto(e1)
                    return render_template('AdminProfile.html',photo=image, msg="Data Saved")
                else:
                    return render_template('AdminProfile.html', msg="Error : Try again")
            else:
                #fetch the data of logged in admin
                sql="select * from admindata where email='"+e1+"'"
                cur=userdb()
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    image=checkphoto(e1)
                    data=cur.fetchone()
                    return render_template('AdminProfile.html',photo=image,data=data)
                else:
                    return render_template('AdminProfile.html',msg="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/student_profile',methods=['GET','POST'])
def student_profile():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='student':
            if request.method=='POST':
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']
                photo=checkphoto(e1)
                cur=userdb()
                sql="update admindata set name='"+name+"',address='"+address+"',contact='"+contact+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    image = checkphoto(e1)
                    return render_template('StudentProfile.html',photo=image, msg="Data Saved")
                else:
                    return render_template('StudentProfile.html', msg="Error : Try again")
            else:
                #fetch the data of logged in admin
                sql="select * from studentdata where email='"+e1+"'"
                cur=userdb()
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    image=checkphoto(e1)
                    data=cur.fetchone()
                    return render_template('StudentProfile.html',photo=image,data=data)
                else:
                    return render_template('StudentProfile.html',msg="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/about')
def about():
    return render_template('About.html')

"""@app.route('/adminphoto')
def adminphoto():
    return render_template('photoupload_admin.html')"""

@app.route('/adminphoto1', methods=['GET','POST'])
def adminphoto1():
    if 'usertype' in session:
        ut = session['usertype']
        e1 = session['email']
        if ut == 'admin':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cur = userdb()
                    sql="insert into photodata values('"+e1+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n==1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('photoupload_admin.html',result="Success")
                        else:
                            return render_template('photoupload_admin.html', result="Failure")
                    except:
                        return render_template('photoupload_admin.html', result="Duplicate")
                else:
                    return render_template('photoupload_admin.html')
            else:
                return render_template("photoupload_admin.html")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/studentphoto1', methods=['GET','POST'])
def studentphoto1():
    if 'usertype' in session:
        ut = session['usertype']
        e1 = session['email']
        if ut == 'student':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cur = userdb()
                    sql="insert into photodata values('"+e1+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n==1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('photoupload_student.html',result="Success")
                        else:
                            return render_template('photoupload_student.html', result="Failure")
                    except:
                        return render_template('photoupload_student.html', result="Duplicate")
                else:
                    return render_template('photoupload_student.html')
            else:
                return render_template("photoupload_student.html")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/studentchangephoto', methods=['GET','POST'])
def studentchangephoto():
    if 'usertype' in session:
        ut = session['usertype']
        e1 = session['email']
        if ut == 'student':
            if request.method == 'POST':
                file = request.files['F2']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cur = userdb()
                    sql="update photodata set photo='"+filename+"' where email='"+e1+"'"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n==1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('ChangeStudentPhoto.html',result="Success")
                        else:
                            return render_template('ChangeStudentPhoto.html', result="Failure")
                    except:
                        return render_template('ChangeStudentPhoto.html', result="Duplicate")
                else:
                    return render_template('ChangeStudentPhoto.html')
            else:
                return render_template("ChangeStudentPhoto.html")
        if ut == 'admin':
            if request.method == 'POST':
                file = request.files['F2']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cur = userdb()
                    sql="update photodata set photo='"+filename+"' where email='"+e1+"'"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n==1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('ChangeAdminPhoto.html',result="Success")
                        else:
                            return render_template('ChangeAdminPhoto.html', result="Failure")
                    except:
                        return render_template('ChangeAdminnPhoto.html', result="Duplicate")
                else:
                    return render_template('ChangeAdminPhoto.html')
            else:
                return render_template("ChangeAdminPhoto.html")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/update',methods=['GET','POST'])
def update():
    if 'usertype' in session:
        ut = session['usertype']
        e1 = session['email']
        if ut == 'student':
            if request.method == 'POST' :
                solution = request.form['T1']
                qid = request.form['qid']
                solby = e1
                soldate = str(int(time.time()))
                sql = "update solutions set solution='"+solution+"' where sid='"+sid+"'"
                cur = userdb()
                cur.execute(sql)
                n = cur.rowcount
                msg = "Error: Try again"
                if n>1:
                    msg = "Solution Updated"
                return render_template('Update.html', msg=msg)
            else:
                return redirect(url_for('solve'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


if(__name__=='__main__'):
    app.run(debug=True)