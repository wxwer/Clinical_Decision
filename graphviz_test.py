# -*- coding: utf-8 -*-

from graphviz import Digraph
import os
import pymysql as mq
from Stack import *


sql1 = "select * from node1 where description=%s"
sql2 = "select * from edge1 where start_id=%s"
sql3 = "select * from node1 where id=%s"
sql4 = "select * from node2 where parent_id=%s"
sql5 = "select * from edge2 where start_id=%s"
sql6 = "select * from edge1 where label=%s and start_id=%s"
sql7 = "select * from node3 where label=%s and parent_id=%s"



os.environ['PATH']
try:
    db=mq.connect("localhost","root","950823","grakn")
    cursor = db.cursor(mq.cursors.DictCursor)
except:
    print('连接数据库失败')


def createGraphFromRoot(r_id,cur):
    dot=Digraph(name='MyPicture',comment='the test',format='png')
    cur.execute(sql3,r_id)
    node=cur.fetchall()[0]
    id=node['id']
    ss=Stack()
    dot.node(str(id),node['description'],color='red',fontname="SimSun")
    cur.execute(sql6,['next',id])
    rlts=cursor.fetchall()
    ss.pushsq(rlts)
    while(not ss.is_empty()):
        rlt=ss.pop()
        check=rlt['next_check']
        start_id=rlt['start_id']
        end_id=rlt['end_id']
        cursor.execute(sql3,end_id)
        node=cursor.fetchall()[0]
        dot.node(str(end_id),node['description'],fontname="SimSun")
        dot.edge(str(start_id),str(end_id),label=rlt['next_check'],fontname="SimSun")
        id=node['id']
        cursor.execute(sql6,['next',id])
        rlts=cursor.fetchall()
        if(len(rlts)>0):
            ss.pushsq(rlts)
    dot.view()
createGraphFromRoot(1,cursor)
