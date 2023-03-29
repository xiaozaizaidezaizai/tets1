# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：miMa.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/2 20:23 
'''
import hashlib
def md5(s, salt='gytwl!@#$'):
    '''
    对用户密码进行哈希处理
    '''
    s = (str(s) + salt).encode('utf-8')
    return hashlib.md5(s).hexdigest()


print(md5(12))
sql = "select usr from account where usr = '%s'" % ('AAA')
print(sql)