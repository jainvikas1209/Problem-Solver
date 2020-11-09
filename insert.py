import pymysql

conn=pymysql.connect(host='localhost',user='root',db='employee',passwd='',autocommit=True)
cur=conn.cursor()
username=input("enter username")
rollno=input("enter rollno")
name=input("enter name")
email=input("enter email")
sql="insert into student values('"+username+"','"+rollno+"','"+name+"','"+email+"')"
print(sql)
cur.execute(sql)
n=cur.rowcount
if(n==1):
    print("data stored")
else:
    print("Try again..!!")
