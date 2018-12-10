# -*- coding: utf-8 -*-

from gl import *
from wrap.base import *
from openpyxl import Workbook
from openpyxl import load_workbook

class Business:

    def __init__(self):
        self.db = DB(db='wanbo')
        self._tables = {'测试':'test','收支明细':'balance','应收账款':'account','合同明细':'contract','开票明细':'invoice'}
        self._stats = ['应收账款统计','开票统计','收支统计']
        self._statsAccount = {
            '今年合同额':{'row':0,'column':0,'form':None},
            '历年合同额':{'row':0,'column':1,'form':None},
            '合同总额':{'row':0,'column':2,'form':None},
            '今年回款额':{'row':2,'column':0,'form':None},
            '历年回款额':{'row':2,'column':1,'form':None},
            '回款总额':{'row':2,'column':2,'form':None},
            '今年未收款额':{'row':4,'column':0,'form':None},
            '历年未收款额':{'row':4,'column':1,'form':None},
            '未收款总额':{'row':4,'column':2,'form':None},
            '正常欠款':{'row':4,'column':3,'form':None},
            '异常欠款':{'row':4,'column':4,'form':None},
            '到期欠款':{'row':4,'column':5,'form':None},
            '今年坏账额':{'row':6,'column':0,'form':None},
            '历年坏账额':{'row':6,'column':1,'form':None},
            '坏账总额':{'row':6,'column':2,'form':None},
            '今年提成额':{'row':8,'column':0,'form':None},
            '历年提成额':{'row':8,'column':1,'form':None},
            '提成总额':{'row':8,'column':2,'form':None},
            '今年合同欠款率':{'row':10,'column':0,'form':'百分比'},
            '历年合同欠款率':{'row':10,'column':1,'form':'百分比'},
            '总欠款率':{'row':10,'column':2,'form':'百分比'}
        }

    def __del__(self):
        if self.db != None:
            del self.db
            self.db = None

    def tables(self):
        return self._tables

    def stats(self):
        return self._stats

    def statsAccount(self):
        return self._statsAccount

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

    def getInsertTemplates(self, table, enHead):
        prefix = 'insert into %s (' % table
        suffix = 'values('
        #编号由数据库自动生成，所以从1开始
        for n in range(1, len(enHead)):
            prefix += '%s,' % enHead[n]
            suffix += '%TBD,'
        return '%s) %s)' % (prefix.rstrip(','),suffix.rstrip(','))

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
        table = self.tables()[tableZh]
        head = self.selectTableHead(table)
        sql = self.getInsertTemplates(table, head[0])
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

    def getContractAmount(self, alias, condition=None):
        if condition == None:
            sql = 'select sum(amount) as %s from contract' % alias
        else:
            sql = 'select sum(amount) as %s from contract where %s' % (alias,condition)
        return self.db.query(sql)

    def getAccountStats(self):
        mp = {}
        sql = 'select sum(amount)as"合同总额",sum(paid)as"回款总额",sum(unpaid)as"未收款总额",sum(debt)as"坏账总额",sum(commission)as"提成总额" from account'
        mp.update(self.db.query(sql)[0])
        sql = 'select sum(amount)as"今年合同额",sum(paid)as"今年回款额",sum(unpaid)as"今年未收款额",sum(debt)as"今年坏账额",sum(commission)as"今年提成额" from account where year(date)=year(now())'
        mp.update(self.db.query(sql)[0])
        sql = 'select sum(amount)as"历年合同额",sum(paid)as"历年回款额",sum(unpaid)as"历年未收款额",sum(debt)as"历年坏账额",sum(commission)as"历年提成额" from account where year(date)<year(now())'
        mp.update(self.db.query(sql)[0])
        sql = 'select sum(unpaid)as"正常欠款" from account where status="正常欠款"'
        mp.update(self.db.query(sql)[0])
        sql = 'select sum(unpaid)as"异常欠款" from account where status="异常欠款"'
        mp.update(self.db.query(sql)[0])
        sql = 'select sum(unpaid)as"到期欠款" from account where status="到期欠款"'
        mp.update(self.db.query(sql)[0])
        return mp

