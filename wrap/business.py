# -*- coding: utf-8 -*-

from gl import *
from wrap.base import *
from openpyxl import Workbook
from openpyxl import load_workbook

class Business:

    def __init__(self):
        self.db = DB(db='wanbo')
        self._tables = {'测试':'test','收支明细':'balance','应收账款':'account'}
        self._insertTemplates = {
            '收支明细':'insert into balance (account_id,source,class1,class2,date,abstract,income,pay,balance,type,credence,remark) \
                values(%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD)',
            '测试':'insert into test (name,age,date) \
                values(%TBD,%TBD,%TBD)',
            '应收账款':'insert into account (date,seller,contract,client,amount,paid,unpaid,debt,percent,invoice_commission,\
                invoice_type,invoice_paid,invoice_unpaid,status,unpaid_reason,commission,commission_date,remark) \
                values(%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD,%TBD)'
            }

    def __del__(self):
        if self.db != None:
            del self.db
            self.db = None

    def tables(self):
        return self._tables

    def insertTemplates(self):
        return self._insertTemplates

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


