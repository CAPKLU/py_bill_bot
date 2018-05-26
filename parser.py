# -*- coding: utf-8 -*-
# !/usr/bin/python2.7
# vim: set sts=4 et:
from bs4 import BeautifulSoup
import re
import csv
import sys

datail3 = r'busi-other_detail\.tab3-one[\s\S]*busi-other_detail\.tab3-one'
# 截取e时代卡明细的正则表达式


def icbc_Ecard(input_name):
    print(input_name)
    f = open(input_name)
    st = re.search(datail3, f.read())
    soup = BeautifulSoup(st.group()).find("table", "table1")
    rows = []
    for row in soup.find_all("tr"):
        string = []
        for line in row.find_all("td"):
            temp_ = line.get_text()
            temp_ = temp_.strip()
#            temp_ = re.sub(r's+', "", temp_)
            temp_ = re.sub(r'&nbsp', "", temp_)
#            temp_ = re.sub(r'^\+', "", temp_)
            string.append(temp_.encode('utf-8'))
        rows.append(string)
    output_csv(rows, re.sub(r'\.html$', "", input_name))
    f.close()


def output_csv(rows, output_name, flag='a'):
    with open(output_name+'.csv', flag) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)
    csv_file.close()


if __name__ == "__parser__":
    icbc_Ecard(sys.argv[1])
    print("working")
