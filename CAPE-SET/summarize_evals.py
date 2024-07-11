#!/usr/bin/env python3
'''
Given multiple CAPE/SET evaluation raw data XLSX spreadsheets, print summary statistics
Niema Moshiri 2024
'''
from openpyxl import load_workbook
from sys import argv
from xlrd import open_workbook

if __name__ == "__main__":
    # load data
    assert len(argv) != 1, "USAGE: %s <CAPE/SET.xlsx> [CAPE/SET.xls(x) 2] [...]" % argv[0]
    data = dict() # data[question][response] = count
    for fn in argv[1:]:
        wb = load_workbook(filename=fn); ws = wb.worksheets[0]; header = None
        for row_num, row in enumerate(ws.values):
            row_s = [s.strip() for s in row]
            if(row_num == 0):
                header = row_s
                for q in header:
                    if q not in data:
                        data[q] = dict()
            else:
                for i, r in enumerate(row_s):
                    if r == '':
                        continue # skip empty strings
                    q = header[i]
                    if r not in data[q]:
                        data[q][r] = 0
                    data[q][r] += 1

    # print results
    for q in data:
        if len(data[q]) < 10:
            total = sum(data[q].values())
            print('- %s (%d)' % (q,total))
            for r in sorted(data[q].keys(), key=lambda x: data[q][x], reverse=True):
                print('  - %s: %d (%0.2f%%)' % (r, data[q][r], 100*data[q][r]/total))
