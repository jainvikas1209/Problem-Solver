import pymysql

def userdb():
    conn = pymysql.connect(passwd='', host='localhost', user='root', port=3306, db='studs', autocommit=True)
    cur = conn.cursor()
    return cur


def checkphoto(email):
    cur = userdb()
    cur.execute("select * from photodata where email='"+email+"'")
    n=cur.rowcount
    photo="NO"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo


def getsolutions(qid):
    cur=userdb()
    sql="select * from solutions where qid="+str(qid)+" order by soldate desc"
    cur.execute(sql)
    n=cur.rowcount
    data="no"
    if n>0:
        data=cur.fetchall()
    return data