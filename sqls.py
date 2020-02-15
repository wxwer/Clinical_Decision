# -*- coding: utf-8 -*-

sql1 = "select * from node1 where description=%s"
sql2 = "select * from edge1 where start_id=%s"
sql3 = "select * from node1 where id=%s"
sql4 = "select * from node2 where parent_id=%s"
sql5 = "select * from edge2 where start_id=%s"
sql6 = "select * from edge1 where label=%s and start_id=%s"
sql7 = "select * from node3 where label=%s and parent_id=%s"
sql8 = "select * from edge1 where next_check=%s"
sql9 = "select * from edge1 where id=%s"
#从检查表中根据检查名获取到相应地检查项目
sql10 = "select * from checkitems where ck_name=%s"
#从属性表中根据属性名获取到相应地取值集合
sql11 = "select * from valueset where key1=%s"
sql12 = "select * from node3 where label=%s and id=%s"