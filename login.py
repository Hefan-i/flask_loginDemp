import flask,json
from flask import request
import pymysql

'''
flask 简单登录接口

'''
server =flask.Flask(__name__)

def get_conn():
    #建立连接
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='woshibenzhu20131',db='user',charset='utf8')
    #创建游标
    cursor =conn.cursor()
    return conn,cursor

def close_conn(conn,cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
def query(sql,*args):
    conn,cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    conn.commit()
    close_conn(conn,cursor)
    return res

def get_user(username,password):
    sql = "select id from users where username ='" + username + "' and password = '" + password + "'"
    res =query(sql)
    return res


@server.route('/login',methods=['get','post'])
def login():
    username = request.values.get('name')
    pwd = request.values.get('pwd')
    res = get_user(username,pwd)
    if res:
        resu = {'code':200,'message':'ok'}
        return json.dumps(resu,ensure_ascii=False)

    else:
        resu = {'code': -1, 'message': '密码错误'}
        return json.dumps(resu, ensure_ascii=False)

if __name__=='__main__':
   server.run(debug=True,port=10000,host='127.0.0.1')