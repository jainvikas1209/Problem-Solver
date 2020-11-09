import pymysql

conn=pymysql.connect(host='localhost',user='root',db='studs',passwd='',autocommit=True)
cur=conn.cursor()
sql="select * from student"
print(sql)
cur.execute(sql)
n=cur.rowcount
if(n>0):
    data=cur.fetchall()
    for a in data:
        print(a[0],"\t",a[1],"\t",a[2],"\t",a[3],"\t")
else:
    print("Try again..!!")
