#!/usr/bin/env python3
'''
Given a codePost grade/score report, reorder the points to be in the same order as the given roster file
Niema Moshiri 2019
'''
from os.path import isfile

# main function
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', '--roster', required=True, type=str, help="Roster (TSV) (Last, First, Email, PID, Stepik, iClicker, Grade ID)")
    parser.add_argument('-g', '--grades', required=True, type=str, help="codePost Grade/Score Report (CSV) (Email, Points)")
    parser.add_argument('-o', '--output', required=False, type=str, default="stdout", help="Output File")
    args = parser.parse_args()
    if args.output == 'stdout':
        from sys import stdout as outfile
    else:
        assert not isfile(args.output), "Output file exists: %s" % args.output
        outfile = open(args.output,'w')

    # load codePost points
    points = dict()
    for l in open(args.grades):
        if l.startswith('Student,'):
            continue
        e,p = [v.strip() for v in l.strip().split(',')]
        if len(p) == 0:
            p = '0'
        points[e] = str(float(p)).rstrip('0').rstrip('.')

    # parse roster and output
    for l in open(args.roster):
        if l.startswith("Last Name\t"):
            continue
        last,first,email,pid,stepik,iclicker = [v.strip() for v in l.strip().split('\t')][:6]
        if email not in points:
            points[email] = '0'
        outfile.write('\t'.join([v.strip() for v in l.strip().split('\t')][:6]))
        outfile.write('\t%s\n' % points[email])
