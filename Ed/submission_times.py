#!/usr/bin/env python3
'''
Given one or more Ed Quiz Response CSVs, create a TSV containing the submission times for all questions for all students
Niema Moshiri 2024
'''
from csv import reader
from os.path import isfile
ROW_SKIP = {'', 'email', 'submissions'}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output submission times TSV")
    parser.add_argument('in_files', metavar='ed_csv', type=str, nargs='+', help="Input Ed Quiz Response CSV(s)")
    args = parser.parse_args()
    for fn in args.in_files:
        if not isfile(fn):
            raise ValueError("File not found: %s" % fn)

    # parse submission times
    times = dict() # times[email][fn] = list of submission times for student `email` in `fn`
    num_questions = dict() # num_questions[fn] = number of questions in `fn`
    for fn in args.in_files:
        for row in reader(open(fn)):
            if row[0].strip().lower() in ROW_SKIP:
                continue
            email = row[0].strip(); ind = 9
            if email not in times:
                times[email] = dict()
            if fn not in times[email]:
                times[email][fn] = list()
            while ind < len(row):
                times[email][fn].append(row[ind].strip()); ind += 4
            if fn not in num_questions:
                num_questions[fn] = len(times[email][fn])

    # write output
    if args.output == 'stdout':
        from sys import stdout; args.output = stdout
    else:
        args.output = open(args.output, 'w')
    args.output.write('Student\t%s\n' % '\t'.join('%s Q%d' % (fn, i+1) for fn in args.in_files for i in range(num_questions[fn])))
    for email in times:
        args.output.write('%s\t%s\n' % (email, '\t'.join(t for fn in args.in_files for t in times[email][fn])))

    # finish up
    args.output.close()
