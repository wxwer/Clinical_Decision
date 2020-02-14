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
sql8 = "select * from edge1 where next_check=%s"
sql9 = "select * from edge1 where id=%s"

s1={'check':'左室检查','n_prpt':1,'value':[('左室','扩张')]}
s2={'check':'肌小梁等检查1','n_prpt':5,'value':[('肌小梁','增多'),('非致密心肌','增多'),\
            ('致密心肌','变薄'),('NC/C',5),('CDFI','可见')]}
s3={'check':'肌小梁增生运动检查','n_prpt':1,'value':[('肌小梁增生的左室壁心肌运动','减低')]}
s4={'check':'右室检查','n_prpt':1,'value':[('右室','正常')]}
fts=[s1,s2,s3,s4]

os.environ['PATH']
try:
    db=mq.connect("localhost","root","950823","grakn")
    cursor = db.cursor(mq.cursors.DictCursor)
except:
    print('连接数据库失败')

#根据输入的检查项目以及临床路径，判断出可能缺少的检查项目
#注：只能判断出中间缺少的，不能判断出后续缺少的
def detectLackFeatures(fts,cursor,is_view=True):
    cks=[ft['check'] for ft in fts]
    cks.append('心内膜检查')
    dot=Digraph(name='LackFeatures',comment='the test',format='png')
    dot.node('root',label='ROOT',color='blue')
    edge_set=[]
    node_set=[]
    for ck in cks:
        cursor.execute(sql8,ck)
        rlts=cursor.fetchall()
        if(len(rlts)==0):
            print(ck+'不存在')
            continue
        for rlt in rlts:
            id=rlt['id']
            if(not str(id) in node_set):
                dot.node(str(id),rlt['next_check'],color='blue',fontname="SimSun")
                node_set.append(str(id))
            parent_id=rlt['parent_id']
            if(parent_id==None):
                if(not ('root',str(id)) in edge_set):
                    dot.edge('root',str(id),fontname="SimSun")
                    edge_set.append(('root',str(id)))
            while(parent_id!=None):
                cursor.execute(sql9,parent_id)
                rlt_p=cursor.fetchall()[0]
                not_lack=rlt_p['next_check'] in cks
                if(not_lack):
                    if(not str(rlt_p['id']) in node_set):
                        dot.node(str(rlt_p['id']),rlt_p['next_check'],color='blue',fontname="SimSun")
                        node_set.append(str(rlt_p['id']))
                else:
                    if(not str(rlt_p['id']) in node_set):
                        dot.node(str(rlt_p['id']),rlt_p['next_check'],color='red',fontname="SimSun")
                        node_set.append(str(rlt_p['id']))
                if(not (str(rlt_p['id']),str(id)) in edge_set):
                    dot.edge(str(rlt_p['id']),str(id),fontname="SimSun")
                    edge_set.append((str(rlt_p['id']),str(id)))
                id=parent_id
                parent_id=rlt_p['parent_id']
                if(parent_id==None):
                    if(not ('root',str(id)) in edge_set):
                        dot.edge('root',str(id),fontname="SimSun")
                        edge_set.append(('root',str(id)))
    if is_view:
        dot.view()
    else:
        dot.render()
detectLackFeatures(fts,cursor)