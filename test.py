from gl import *
from wrap import *
from openpyxl import Workbook
from openpyxl import load_workbook
import pymysql.cursors

GL.LOG = getLogger('WanboLoger', 'logs', 'console.log')
db = DB(db='wanbo')

def InsertToBalance(mp):
    keys_sql = '('
    values_sql = '('
    for k,v in mp.items():
        keys_sql += '%s,' % k
        if v == None:
            values_sql += 'NULL,'
        elif isinstance(v, str):
            values_sql += '\'%s\',' % v
        else:
            values_sql += '%s,' % v
    keys_sql = keys_sql.rstrip(',')
    values_sql = values_sql.rstrip(',')
    keys_sql += ')'
    values_sql += ')'
    #sql = 'insert into balance %s values%s' % (tuple(mp.keys()), tuple(mp.values()))
    sql = 'insert into balance %s values%s' % (keys_sql,values_sql)
    #print(sql)
    #sql = sql.replace('None', 'NULL')
    db.exec(sql)

def TestDB():
    sql = 'select * from test'
    print(db.query(sql))

def ReadBalanceData(source):
    n = 0
    mp = {}
    for row in ws.rows:
        n = n + 1
        if n <= 3:
            continue
        if n == 10:
            break
        if len(row) < 12:
            return
        mp['class1'] = row[0].value
        if mp['class1']==None or mp['class1'].strip()=='':
            return
        mp['class2'] = row[1].value
        year = row[2].value
        month = row[3].value
        day = row[4].value
        mp['date'] = '%d-%d-%d' % (year,month,day)
        mp['abstract'] = row[5].value
        mp['income'] = row[6].value
        mp['pay'] = row[7].value
        mp['balance'] = row[8].value
        mp['type'] = row[9].value
        mp['credence'] = row[10].value
        mp['remark'] = row[11].value
        mp['source'] = source
        InsertToBalance(mp)

fn = '../../db/wanbo/2018万泊财务汇总表（46周）.xlsx'
wb = load_workbook(fn, read_only=True, data_only=True)
for ws in wb:
    if ws.title == '银行明细账':
        source = '建设银行（基本户）'
        ReadBalanceData(source)
    elif ws.title == '现金账户1明细账':
        source = '平安银行（姚洋）'
        ReadBalanceData(source)
    elif ws.title == '现金账户2明细账':
        source = '平安银行（李昱平）'
        ReadBalanceData(source)
    else:
        pass

db.close()
