#encoding: utf-8
'''
Created on 2015年11月16日

@author: lml
'''
import threading
from config.CommonConfig import MYSQL_IP

# -*- coding: UTF-8 -*-
"""
desc:数据库操作类
@note:
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理
"""

import sys
reload(sys)
# sys.setdefaultencoding("utf-8")

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from config.CommonConfig import MYSQL_IP
 
class __config(object):
    pass
 
Config =  __config()
Config.DBHOST  =  MYSQL_IP
Config.DBPORT  = 3306
Config.DBUSER  = "root"
Config.DBPWD = "lml19870419"
Config.DBNAME = "test"
Config.use_unicode=False
Config.DBCHAR="utf8"

class MysqlClient(object):
    """
        MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现
        获取连接对象：conn = MysqlClient.getConn()
        释放连接对象;conn.close()或del conn
    """
    #连接池对象
    __pool = None
    __mutex = None
    def __init__(self):
        """
        数据库构造函数，从连接池中取出连接，并生成操作游标
        """
#        self._conn = MySQLdb.connect(host=Config.DBHOST , port=Config.DBPORT , user=Config.DBUSER , passwd=Config.DBPWD ,
#                              db=Config.DBNAME,use_unicode=False,charset=Config.DBCHAR,cursorclass=DictCursor)
        self._conn = MysqlClient.__getConn()
        self._cursor = self._conn.cursor()
 
    @staticmethod
    def __getConn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if MysqlClient.__pool is None:
            __pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=20 ,
                              host=Config.DBHOST , port=Config.DBPORT , user=Config.DBUSER , passwd=Config.DBPWD ,
                              db=Config.DBNAME,use_unicode=True,charset=Config.DBCHAR,cursorclass=DictCursor)

        if MysqlClient.__mutex is None:
            MysqlClient.__mutex = threading.Lock()

        return __pool.connection()
 
    def getAll(self,sql,param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        if count>0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result
 
    def getOne(self,sql,param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        try:
            MysqlClient.__mutex.acquire()
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql,param)
            if count>0:
                result = self._cursor.fetchone()
            else:
                result = False
        finally:
            MysqlClient.__mutex.release()

        return result
 
    def getMany(self,sql,num,param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        if count>0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result
 
    def insertOne(self,sql,value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self._cursor.execute(sql,value)
        return self.__getInsertId()
 
    def insertMany(self,sql,values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql,values)
        return count
 
    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        if len(result) > 0:
            return result[0]['id']
        else:
            return 0
 
    def __query(self,sql,param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        return count
 
    def update(self,sql,param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql,param)
 
    def delete(self,sql,param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql,param)
 
    def begin(self):
        """
        @summary: 开启事务
        """
#         self._conn.autocommit(0)
 
    def end(self,option='commit'):
        """
        @summary: 结束事务
        """
        if option=='commit':
            self._conn.commit()
        else:
            self._conn.rollback()
 
    def dispose(self,isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd==1:
            self.end('commit')
        else:
            self.end('rollback');
        self._cursor.close()
        self._conn.close()

def fun(client, urls, index):
    if index > 1000:
        return
    sql = "select create_time from published_url where url = %s"
    result = client.getOne(sql, (urls[index]["url"], ))
#     print index
    print result
    
if __name__ == "__main__":
    client = MysqlClient()
#     cursor = client.getAll("select * from published_url")
#     sql = "select create_time from published_url where url = %s"
#     url1 = 'http://news.163.com/15/1124/15/B96QJKMQ00014JB6.html#f=wlist'
#     url2 =  'http://news.163.com/15/1124/16/B96TS88000014JB6.html#f=wlist'
#     urls = client.getAll("select url from published_url")
# #     print urls[0:3]
#     index = 0
#     print len(urls)
#     count = 5
#     while 1:
#         thread_list = []
#         for i in range(count):
#             thread_list.append(threading.Thread(target=fun, args=(client, urls, index)))
#             index = index + 1
#             
#         for thread in thread_list:
#             thread.start()
#             
#         for thread in thread_list:
#             thread.join()
            
#     cursor = client.getOne("select create_time from published_url where url = %s", ('http://news.163.com/15/1124/16/B96TS88000014JB6.html#f=wlist', ))
#     print cursor
#     cursor = client.getOne("select create_time from published_url where url = %s", ('http://news.163.com/15/1124/15/B96QJKMQ00014JB6.html#f=wlist', ))
#     print cursor
#     print cursor
    cursor = client.insertOne("insert into user values(%s,%s)", (33, u"中文"))
    print u"中文".encode("utf8")
    client.end("commit")
    result = client.getAll("select * from user")
    for entry in result:
#        pass 
        entry["email"] = str(entry["email"].encode("utf-8"))
    print result
#     cursor = client.getOne("select * from published_url where url=%s", ('http.//test2', ))
#     print cursor
#     result = client.insertOne("insert into published_url(url, tag, sub_tag) values(%s, %s, %s)",  ("test3", "tag", "sub_tag"))
#     print result