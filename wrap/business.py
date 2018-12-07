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
            '应收账款':'insert into account (date,seller,contract,client,amount,paid,unpaid,debt,percent,remark,\
                invoice_type,invoice_paid,invoice_unpaid,status,unpaid_reason,commission,commission_date,invoice_commission) \
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

    def updateTableById(self, table, field, tp, value, field_id, value_id):
        sql = 'update %s set %s = %TBD where %s = %d' 
        if value.strip() == '':
            sql = sql.replace('%TBD','%s', 1)
            value = 'NULL'
        elif tp == 'int':
            sql = sql.replace('%TBD','%d', 1)
            value = int(value)
        elif tp == 'double':
            sql = sql.replace('%TBD','%.2f', 1)
            value = float(value)
        else:
            sql = sql.replace('%TBD','"%s"', 1)
        sql = sql % (table,field,value,field_id,value_id)
        self.db.exec(sql)

    def insertTable(self, tableZh, itemData):
        GL.LOG.info(itemData)
        sql = self.insertTemplates()[tableZh]
        head = self.selectTableHead(self.tables()[tableZh])
        r = 0
        datas = []
        #编号由数据库自动生成，所以从1开始
        for c in range(1, len(itemData)):
            txt = itemData[c]
            if txt == 'NULL':
                sql = sql.replace('%TBD','%s', 1)
            elif head[2][c] == 'int':
                sql = sql.replace('%TBD','%d', 1)
                txt = int(txt)
            elif head[2][c] == 'double':
                sql = sql.replace('%TBD','%.2f', 1)
                txt = float(txt)
            else:
                sql = sql.replace('%TBD','"%s"', 1)
            datas.append(txt)
        GL.LOG.info(sql)
        GL.LOG.info(datas)
        sql = sql % tuple(datas)
        self.db.exec(sql)
        GL.LOG.info(sql)

