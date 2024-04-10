#!/usr/bin/env python3
'''
Given a Submission Times TSV produced by submission_times.py, (1) add the question numbers to the timestamps, and (2) sort each student's response times chronologically.

Niema Moshiri 2024
'''
from datetime import datetime
from os.path import isfile

def parse_ed_timestamp(s, empty='max'):
    if s == '':
        if empty == 'max':
            return datetime.max
        elif empty == 'min':
            return datetime.min
        else:
            raise ValueError("Invalid empty handling: %s" % empty)
    else:
        return datetime.strptime(s, '%d %b %Y %H:%M:%S %Z')

if __name__ == "__main__":
    # parse user args
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input submission times TSV")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output sorted submission times TSV")
    args = parser.parse_args()
    if args.input.lower().strip() == 'stdin':
        from sys import stdin as infile
    elif not isfile(args.input):
        raise ValueError("File not found: %s" % args.input)
    else:
        infile = open(args.input)
    if args.output.lower().strip() == 'stdout':
        from sys import stdout as outfile
    elif isfile(args.output):
        raise ValueError("Output file exists: %s" % args.output)
    else:
        outfile = open(args.output, 'w')

    # parse and sort submission times
    header = None
    for row_num, row in enumerate(infile):
        parts = [v.strip() for v in row.split('\t')]
        if row_num == 0:
            header = parts
        else:
            sorted_row = [parts[0]] + sorted(('%s (%s)' % (parts[i], header[i]) for i in range(1, len(header))), key=lambda x: parse_ed_timestamp(' ('.join(', '.join(x.split(', ')[1:]).split(' (')[:-1]).strip()))
            outfile.write('%s\n' % '\t'.join(sorted_row))
    infile.close(); outfile.close()
