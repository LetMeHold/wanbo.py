# -*- coding: utf-8 -*-

from gl import *
from wrap.base import *
from openpyxl import Workbook
from openpyxl import load_workbook

class Business:

    def __init__(self):
        self.db = DB(db='wanbo')
        self.tol = Tools()

    def __del__(self):
        if self.db != None:
            del self.db
            self.db = None

    def selectTableHead(self, table):
        sql = 'select %s_en,%s_zh,%s_tp from head where %s_en is not null' % (table,table,table,table)
        ret = self.db.query(sql)
        en = []
        zh = []
        tp = []
        for r in ret:
            en.append(r['%s_en' % table])
            zh.append(r['%s_zh' % table])
            tp.append(r['%s_tp' % table])
        return (en,zh,tp)

    def selectTableData(self, table):
        sql = 'select * from %s' % table
        return self.db.query(sql)

    def execSql(self, sql):
        self.db.exec(sql)

