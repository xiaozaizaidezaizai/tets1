# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：util.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/2 20:16 
'''
'''
数据库连接是的工具
登录时密码加密

'''
import pymysql, hashlib
import Database.mysql_data as mydata#引入数据

def md5(s, salt='gytwl!@#$'):#对用户密码进行哈希处理
    s = (str(s) + salt).encode('utf-8')
    return hashlib.md5(s).hexdigest()


class Database(object): #连接数据库
    '''
    连接数据库
    '''
    def __init__(self, mysql_info):
        self._connection = pymysql.connect(**mysql_info)
        '''**这两个符号决定了传入的参数必须是字典类型'''
        print(self._connection)
        print(type(self._connection))#操作数据库的类

    def __del__(self):#断开连接
        self._connection.close()

    def _execute(self, query):# ' qyery==sql ' 返回执行语句的查询结果
        try:
            cursor = self._connection.cursor()
            cursor.execute(query) # 创建游标 执行SQL查询
            s = query.split()[0]#截取第一个字符串
            print('s='+s)# s=select
            res = None
            if s == 'update' or s == 'insert' or s == 'delete':
                self._connection.commit()#这是一个 Python 数据库连接对象的方法，用于提交当前事务的所有更改。
                cursor.close()
            elif s == 'select':
                res = cursor.fetchall()# 获取所有的行
                print("数据：")
                print(res)
                cursor.close()
            return (True, res)
        except Exception as e:
            self._connection.rollback()
            return (False, e)

db=Database(mydata.my_data())#传入将数据库信息

def op_mysql(sql:str):#加':'是建议传入的类型为str
    '''在此方法中利用db对象变量调用他自生的方法'''
    return db._execute(sql)#

def Data_Login(usr, pwd):
    '''
    登录情况处理:
    先进行比较用户，再接着比较密码
    1 用户密码正确
    0 数据库错误
    -1 用户不存在
    -2 密码错误
    '''
    usr = md5(usr)
    pwd = md5(pwd)#用户和密码都进行加密后再进行查询

    sql = "select usr from account where usr = '%s'" % (usr)#查询
    flag, res = op_mysql(sql)

    if flag == False:
        return 0  # 数据库错误
    if len(res) == 0:
        print('用户不存在')
        return -1  # 用户不存在

    sql = "select pwd from account where usr = '%s'" % (usr)
    print('查询密码')
    flag, res = op_mysql(sql)
    print(flag)#true
    if flag == False:
        return 0  # 数据库错误
    for x in res:
        if x[0] == pwd:
            return 1  # 密码正确
    if(x[0]!=pwd):
        print('密码错误')
    return -2  # 密码错误

if __name__ == "__main__":
    Data_Login(3,1)