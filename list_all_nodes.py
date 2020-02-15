# -*- coding: utf-8 -*-

from graphviz import Digraph
import os
import pymysql as mq
from Stack import *
from sqls import *
from test_data import *
from get_cursor import *
os.environ['PATH']


#输入某个节点的ID，输出以该节点为根节点的子树

def createGraphFromRoot(r_id,cur):
    dot=Digraph(name='./image/createGraphFromRoot',comment='the test',format='png')
    cur.execute(sql3,r_id)
    node=cur.fetchall()[0]
    id=node['id']
    ss=Stack()
    dot.node(str(id),node['description'],color='red',fontname="SimSun")
    cur.execute(sql2,id)
    rlts=cursor.fetchall()
    ss.pushsq(rlts)
    while(not ss.is_empty()):
        rlt=ss.pop()
        check=rlt['next_check']
        start_id=rlt['start_id']
        end_id=rlt['end_id']
        if(rlt['label']=='DESE'):
            cursor.execute(sql12,['DESE',end_id])
            node=cursor.fetchall()[0]
            dot.node('e'+str(node['id']),node['description'],fontname="SimSun",color='yellow')
            dot.edge(str(start_id),'e'+str(node['id']),label='疾病',fontname="SimSun",color='yellow')
            
            continue
        elif(rlt['label']=='PROG'):
            cursor.execute(sql12,['PROG',end_id])
            node=cursor.fetchall()[0]
            dot.node('e'+str(node['id']),node['description'],fontname="SimSun",color='yellow')
            dot.edge(str(start_id),'e'+str(node['id']),label='预后',fontname="SimSun",color='yellow')
            continue
        cursor.execute(sql3,end_id)
        node=cursor.fetchall()[0]
        dot.node(str(end_id),node['description'],fontname="SimSun")
        dot.edge(str(start_id),str(end_id),label=rlt['next_check'],fontname="SimSun")
        id=node['id']
        cursor.execute(sql2,id)
        rlts=cursor.fetchall()
        if(len(rlts)>0):
            ss.pushsq(rlts)
    dot.view()
db,cursor=get_cursor()
if(cursor!=None):
    createGraphFromRoot(1,cursor)
    cursor.close()
    db.close()
