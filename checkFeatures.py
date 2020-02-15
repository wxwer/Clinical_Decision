# -*- coding: utf-8 -*-

from graphviz import Digraph
import os
import pymysql as mq
from sqls import *
from test_data import *
from get_cursor import *
os.environ['PATH']




def checkFeatures(fts,cursor):
    flag=True
    for ft in fts:
        ck=ft['check']
        ft_vs=ft['value']
        cursor.execute(sql10,ck)
        ck_rcds=cursor.fetchall()
        if(len(ck_rcds)<1):
            print(ck+'不在数据库中，请检查命名是否正确')
            flag=False
            continue
        ck_rcd=ck_rcds[0]
        ck_items=ck_rcd['items'].split(',')
        if(len(ck_items)!=ck_rcd['n_prpt']):
            ck_items=ck_rcd['items'].split('，')
        for ft_v in ft_vs:
            if(not ft_v[0] in ck_items):
                print(ck+'的 '+ft_v[0]+' 项目不存在，请检查命名')
                flag=False
                continue
            cursor.execute(sql11,ft_v[0])
            vs_rcds=cursor.fetchall()
            if(len(vs_rcds)<1):
                flag=False
                print(ck+'的 '+ft_v[0]+' 项目不存在，请检查命名')
                continue
            vs_rcd=vs_rcds[0]
            ck_item_valueSet=vs_rcd['valueSet'].split(',')
            if(len(ck_item_valueSet)==0):
                ck_item_valueSet=vs_rcd['valueSet'].split('，')
            if(len(ck_item_valueSet)==1 and ck_item_valueSet[0]=='NUMBER'):
                if not (type(ft_v[1])==float or type(ft_v[1])==int):
                    print(ck+'的 '+ft_v[0]+' 取值不在数据库中，请检查取值')
                    print(ck+'的取值为：',ck_item_valueSet)
                    flag=False
                    continue
            elif(not ft_v[1] in ck_item_valueSet):
                print(ck+'的 '+ft_v[0]+' 取值不在数据库中，请检查取值')
                print(ck+'的取值为：',ck_item_valueSet)
                flag=False
                continue
    return flag

db,cursor=get_cursor()
if(cursor!=None):
    flag=checkFeatures(fts,cursor)
    if(flag):
        print('无错误')
cursor.close()
db.close()
        
        