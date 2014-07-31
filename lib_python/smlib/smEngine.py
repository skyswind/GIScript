#coding: utf-8
# 各引擎实现类

import os
import sys
import math
import smData
#import bin.smu as smu
import smu

#UDB类型的数据源
#必填参数：【udb文件路径】
#可先参数：【数据源别名】
class uds(smData.ds):

    #若fileName设为''，则是内存模式
    def __init__(self, fileName, alias = u'ds_udb'):
        smData.ds.__init__(self,alias)
        self.type = u'sceUDB'
        self.fileName = fileName
        
    #打开数据源，若fileName为''，则为内存模式
    def Open(self):
        self.bOpened = smu.OpenDataSource(self.fileName, u"", u"", self.type, self.alias)

        return self.bOpened

    #创建数据源，若fileName为'', 则为内存模式
    def Create(self):
        #若文件已存在，则删除原文件
        if len(self.fileName)>0:
            uddFile = self.fileName.split(u'.')[0] + u'.udd'
            if os.path.exists(self.fileName):
                os.remove(self.fileName)
            if os.path.exists(uddFile):
                os.remove(uddFile)

        self.bOpened = smu.CreateDataSource(self.fileName, u"", u"", self.type, self.alias)
        
        return self.bOpened

#Oracle数据源
#必填参数：【服务名】【用户名】【密码】
#可先参数：【数据源别名】
class oracleds(smData.ds):

    def __init__(self, server, user, pwd, alias = u'ds_oracle'):
        smData.ds.__init__(self, alias)
        self.type = u'sceOraclePlus'
        self.server = server
        self.user = user
        self.pwd = pwd

    def Open(self):
        self.bOpened = smu.OpenDataSource(self.server, self.user, self.pwd, self.type, self.alias)

        return self.bOpened

    def Create(self):
        self.bOpened = smu.CreateDataSource(self.server, self.user, self.pwd, self.type, self.alias)
        
        return self.bOpened

#OracleSpatial数据源
#必填参数：【服务名】【用户名】【密码】
#可先参数：【数据源别名】
class oraclespatialds(smData.ds):

    def __init__(self, server, user, pwd, alias = u'ds_oraclespatial'):
        smData.ds.__init__(self, alias)
        self.type = u'sceOracleSpatial'
        self.server = server
        self.user = user
        self.pwd = pwd

    def Open(self):
        self.bOpened = smu.OpenDataSource(self.server, self.user, self.pwd, self.type, self.alias)

        return self.bOpened

    def Create(self):
        self.bOpened = smu.CreateDataSource(self.server, self.user, self.pwd, self.type, self.alias)
        
        return self.bOpened

#SQL Server数据源
#必填参数：【服务名】【数据库名】【用户名】【密码】
#可先参数：【数据源别名】
class sqlds(smData.ds):

    def __init__(self, server, database, user, pwd, alias = u'ds_sql'):
        smData.ds.__init__(self, alias)
        self.type = u'sceSQLPlus'
        self.server = server
        self.database = database
        self.user = user
        self.pwd = pwd

    def Open(self):
        self.bOpened = smu.OpenDataSource(self.server, self.user, self.pwd, self.type, self.alias, self.database)

        return self.bOpened

    def Create(self):
        self.bOpened = smu.CreateDataSource(self.server, self.user, self.pwd, self.type, self.alias, self.database)
        
        return self.bOpened

#PostgreSQL数据源
#必填参数：【服务名】【数据库名】【用户名】【密码】
#可先参数：【数据源别名】
class pgds(smData.ds):

    def __init__(self, server, database, user, pwd, alias = u'ds_pg'):
        smData.ds.__init__(self, alias)
        self.type = u'scePostgreSQL'
        self.server = server
        self.database = database
        self.user = user
        self.pwd = pwd

    def Open(self):
        self.bOpened = smu.OpenDataSource(self.server, self.user, self.pwd, self.type, self.alias, self.database)

        return self.bOpened

    def Create(self):
        self.bOpened = smu.CreateDataSource(self.server, self.user, self.pwd, self.type, self.alias, self.database)
        
        return self.bOpened

#DB2数据源
#必填参数：【数据库名】【用户名】【密码】
#可先参数：【数据源别名】
class db2ds(smData.ds):

    def __init__(self, database, user, pwd, alias = u'ds_db2'):
        smData.ds.__init__(self, alias)
        self.type = u'sceDB2'
        self.server = u''
        self.database = database
        self.user = user
        self.pwd = pwd

    def Open(self):
        self.bOpened = smu.OpenDataSource(self.server, self.user, self.pwd, self.type, self.alias, self.database)

        return self.bOpened

    def Create(self):
        self.bOpened = smu.CreateDataSource(self.server, self.user, self.pwd, self.type, self.alias, self.database)
        
        return self.bOpened
