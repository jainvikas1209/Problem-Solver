import pymysql

conn=pymysql.connect(host='localhost',user='root',db='studs',passwd='',autocommit=True)
cur=conn.cursor()
username=input("enter username")
roll=input("enter roll")
name=input("enter name")
email=input("enter email")
sql="insert into student values('"+username+"','"+roll+"','"+name+"','"+email+"')"
print(sql)
cur.execute(sql)
n=cur.rowcount
if(n==1):
    print("data stored")
else:
    print("Try again..!!")
