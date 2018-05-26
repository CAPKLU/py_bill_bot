#!/usr/bin/python2.7
# coding=utf-8
# vim: set sts=4 et:

import csv
import sys
import mysql.connector
import ConfigParser
import time
from itertools import islice
import re
import pdb


def import_csv2mysql(input_csv=sys.argv[1], new_table_name="None"):
    sql_cur = csv2mysql()
    new_table_name = sql_cur.creat_table(new_table_name)
    with open(input_csv) as csv_file:
        f_csv = csv.reader(csv_file)
        header = csv.reader(csv_file).next()
        sql = ("INSERT INTO %s" % (new_table_name),
               "(%s) " % (header),
               "VALUES (%s)" % ("%s,%s,%s,%s,%s,%s,%s,%d,%d,%d,%d"))
        print(sql)
        for row in islice(f_csv, 1, None):
            for i in range(7, 10+1):
                tem = re.sub(r',+', "", row[i])
                tem = re.findall(r'[+-]?\d+[\.]?\d+', tem)
                pdb.set_trace()
                if len(tem) != 0:
                    row[i] = float(tem[0])
            param = row
            sql_cur.import_data(sql, param)
        print(f_csv)


class csv2mysql:
    user = ""
    psw = ""
    host = ""
    db = ""

    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read("./pbb.conf")
        conf_local = 'Mysql'
        self.user = cf.get(conf_local, "user")
        self.psw = cf.get(conf_local, "password")
        self.host = cf.get(conf_local, "host")
        self.db = cf.get(conf_local, "database")
        self.conn = mysql.connector.connect(user=self.user,
                                            password=self.psw,
                                            host=self.host,
                                            database=self.db)
        self.cur = self.conn.cursor()
        print(type(self.cur))
# 获得数据库指针

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def creat_table(self, name):
        if(name is "None"):
            new_table_name = time.strftime("%y%m", time.localtime())

        query = "CREATE TABLE IF NOT EXISTS `%s` LIKE icbc_template" \
            % (new_table_name)
        self.cur.execute(query)
        return new_table_name

    def import_data(self, query, param):
        self.cur.execute(query, param)


import_csv2mysql()
