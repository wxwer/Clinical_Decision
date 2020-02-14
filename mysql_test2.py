# -*- coding: utf-8 -*-


import pymysql as mq
from Stack import *
from graphviz import Digraph



 
# SQL 查询语句
sql1 = "SELECT * from node1 where description=%s"
sql2 = "select * from edge1 where start_id=%s"
sql3 = "select * from node1 where id=%s"
sql4 = "select * from node2 where parent_id=%s"
sql5 = "select * from edge2 where start_id=%s"
sql6 = "select * from edge1 where label=%s and start_id=%s"
sql7 = "select * from node3 where label=%s and parent_id=%s"

s1={'check':'左室检查','n_prpt':1,'value':[('左室','扩张')]}
s2={'check':'肌小梁等检查1','n_prpt':5,'value':[('肌小梁','增多'),('非致密心肌','增多'),\
            ('致密心肌','变薄'),('NC/C',5),('CDFI','可见')]}
s3={'check':'肌小梁增生运动检查','n_prpt':1,'value':[('肌小梁增生的左室壁心肌运动','减低')]}
s4={'check':'右室检查','n_prpt':1,'value':[('右室','正常')]}



fts=[s1,s2,s3,s4]

c1={'check':'左室检查','n_prpt':1,'value':['左室']}
c2={'check':'肌小梁等检查1','n_prpt':5,'value':['肌小梁','非致密心肌','致密心肌','NC/C','CDFI']}
c3={'check':'肌小梁增生运动检查','n_prpt':1,'value':['肌小梁增生的左室壁心肌运动']}
c4={'check':'右室检查','n_prpt':1,'value':['右室']}
cks=[c1,c2,c3,c4]


def diagnose(nodes):
    if(len(nodes)==0):
        print('can not diagnose')
    else:
        for node in nodes:
            if(node['label']=='DESE'):
                print('---------------------确诊疾病-------------------------')
                print(node['description'])
            elif(node['label']=='PROG'):
                print('---------------------疾病预后-------------------------')
                print(node['description'].replace('\r',' '))
            else:
                print('can not diagnose')
    
def get_check(check,cks):
    res=None
    for ck in cks:
        if(ck['check']==check):
            res=ck
            break
    return res
def get_feature(check,fts):
    res=None
    for ft in fts:
        if(ft['check']==check):
            res=ft
            break
    return res

def get_feature_from_search(check,prpts):
    res={}
    res['check']=check
    res['n_prpt']=len(prpts)
    value=[]
    for prpt in prpts:
        value.append((prpt['key'],prpt['value'],prpt['type']))
    res['value']=value
    return res

def get_value_from_key(sqs,key):
    res=None
    for sq in sqs:
        if(len(sq)>1 and sq[0]==key):
            res=sq
            break
    return res
             
def is_equal(ck,search_feature,give_feature):
    
    if(not (ck['n_prpt']==search_feature['n_prpt']==search_feature['n_prpt'])):
        print('数据长度不匹配')
        print(ck['check']+','+search_feature['check']+','+give_feature['check'])
        return False
    ck_value=ck['value']
    flag=True
    for ck_v in ck_value:
        s_f=get_value_from_key(search_feature['value'],ck_v)
        g_f=get_value_from_key(give_feature['value'],ck_v)
        if(s_f[2]==None or s_f[2]==''):
            if(s_f[1]!=g_f[1]):
                flag=False
                break
        else:
            if(s_f[2]=='gt'):
                flag=float(g_f[1])>float(s_f[1])
                break
            elif(s_f[2]=='lt'):
                flag=float(g_f[1])<float(s_f[1])
                break
            elif(s_f[2]=='eq'):
                flag=float(g_f[1])==float(s_f[1])
                break
    return flag
    
    
try:
    db=mq.connect("localhost","root","950823","grakn")
    cursor = db.cursor(mq.cursors.DictCursor)
except:
    print('连接数据库失败')



str1='四腔心'
ss=Stack()
#
dot=Digraph(name='MyPicture',comment='the test',format='png')

cursor.execute(sql1,str1)
nodes = cursor.fetchall()
node=nodes[0]
id=node['id']
#
dot.node(str(id),node['description'],color='red',fontname="SimSun")
cursor.execute(sql2,id)
rlts=cursor.fetchall()
ss.pushsq(rlts)
while(not ss.is_empty()):
    rlt=ss.pop()
    check=rlt['next_check']
    start_id=rlt['start_id']
    end_id=rlt['end_id']
    if(rlt['label']=='DESE'):
        dot.node('end','确诊',fontname="SimSun",color='yellow')
        dot.edge(str(start_id),'end',label='疾病',fontname="SimSun",color='blue')
        cursor.execute(sql7,['DESE',start_id])
        nodes=cursor.fetchall()
        diagnose(nodes)
        continue
    elif(rlt['label']=='PROG'):
        dot.node('end','确诊',fontname="SimSun",color='yellow')
        dot.edge(str(start_id),'end',label='预后',fontname="SimSun",color='blue')
        cursor.execute(sql7,['PROG',start_id])
        nodes=cursor.fetchall()
        diagnose(nodes)
        continue
    
    ck=get_check(check,cks)
    if(ck==None):
        print(check+'不存在')
        continue
    cursor.execute(sql3,end_id)
    node=cursor.fetchall()[0]
    id=node['id']
    
    if(node['n_prpt']==1):
        search_feature={'check':node['check'],'n_prpt':1,'value':[(node['key'],node['value'],node['type'])]}
            
    else:
        cursor.execute(sql4,node['id'])
        prpts=cursor.fetchall()
        search_feature=get_feature_from_search(check,prpts)
    give_feature=get_feature(check,fts)
    is_eq=is_equal(ck,search_feature,give_feature)
    if(not is_eq):
        print(check+'诊断不匹配')
        #
        dot.node(str(id),node['description'],fontname="SimSun",color='green')
        dot.edge(str(start_id),str(end_id),label=rlt['next_check'],fontname="SimSun",color='green')
        continue
    else:
        print(check+'匹配')
        #
        dot.node(str(id),node['description'],fontname="SimSun",color='blue')
    dot.edge(str(start_id),str(end_id),label=rlt['next_check'],fontname="SimSun",color='blue')
    cursor.execute(sql2,id)
    rlts=cursor.fetchall()
    if(len(rlts)>0):
        ss.pushsq(rlts)
 
print ("over...")
dot.view()   
cursor.close()
db.close()
