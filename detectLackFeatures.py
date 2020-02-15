# -*- coding: utf-8 -*-

from graphviz import Digraph
import os
import pymysql as mq
from Stack import *
from sqls import *
from test_data import *
from get_cursor import *
os.environ['PATH']

#根据输入的检查项目以及临床路径，判断出可能缺少的检查项目
#注：只能判断出中间缺少的，不能判断出后续缺少的
def detectLackFeatures(fts,cursor,is_view=True):
    cks=[ft['check'] for ft in fts]
    cks.append('心内膜检查')
    dot=Digraph(name='./image/LackFeatures',comment='the test',format='png')
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
db,cursor=get_cursor()
if(cursor!=None):
    detectLackFeatures(fts,cursor)
    cursor.close()
    db.close()