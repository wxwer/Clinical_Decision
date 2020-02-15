# -*- coding: utf-8 -*-
import pymysql as mq


def get_cursor(host="localhost",user="root",password="950823",database="grakn"): 
    cursor=None
    db=None
    try:
        db=mq.connect(host,user,password,database)
        cursor = db.cursor(mq.cursors.DictCursor)
    except Exception as e:
        print('连接数据库失败')
        print(e)
    return db,cursor