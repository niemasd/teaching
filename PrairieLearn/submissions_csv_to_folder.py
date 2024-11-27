#!/usr/bin/env python3
'''
Given a PrairieLearn submissions CSV (ideally "Best Submissions"), convert the contents into a folder structure in which each student has their own subfolder and each submitted file's contents are in its own appropriately-named file.
Niema Moshiri 2024
'''
from base64 import b64decode
from csv import field_size_limit, reader
from gzip import open as gopen
from json import loads as jloads
from os import mkdir
from pathlib import Path
from sys import maxsize

if __name__ == "__main__":
    # set things up
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="PrairieLearn Submissions CSV")
    parser.add_argument('-o', '--output', required=True, type=str, help="Output Directory")
    args = parser.parse_args()
    if args.input == 'stdin':
        from sys import stdin as in_f
    else:
        in_path = Path(args.input)
        if not in_path.is_file():
            raise ValueError("File not found: %s" % in_path)
        elif in_path.name.lower().endswith('.gz'):
            in_f = gopen(in_path, 'rt')
        else:
            in_f = open(in_path, 'r')
    out_path = Path(args.output)
    if out_path.is_dir() or out_path.is_file():
        raise ValueError("Output exists: %s" % out_path)
    mkdir(out_path)
    field_size_limit(maxsize) # for handling large CSVs

    # convert submissions CSV to folder structure
    IND = {'UID':None, 'SUBMITTED ANSWER':None}
    for row_num, row in enumerate(reader(in_f)):
        # parse CSV header
        if row_num == 0:
            for i, k in enumerate([v.strip().upper() for v in row]):
                if k in IND:
                    IND[k] = i
            for k, i in IND.items():
                if i is None:
                    raise ValueError("Key not found in CSV header: %s" % k)

        # parse student row
        else:
            submission = jloads(row[IND['SUBMITTED ANSWER']])
            if '_files' not in submission:
                continue
            student_path = out_path / row[IND['UID']].strip()
            if not student_path.is_dir():
                mkdir(student_path)
            for file_dict in submission['_files']:
                f = open(student_path / file_dict['name'].strip(), 'wb')
                f.write(b64decode(file_dict['contents']))
                f.close()
    in_f.close()
