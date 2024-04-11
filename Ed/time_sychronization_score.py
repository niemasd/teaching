#!/usr/bin/env python3
'''
Given a Submission Times TSV produced by submission_times.py, calculate the Time Synchronization Score.

Niema Moshiri 2024
'''
from datetime import datetime
from os.path import isfile

def parse_ed_timestamp(s):
    return datetime.strptime(s, '%d %b %Y %H:%M:%S %Z')

if __name__ == "__main__":
    # parse user args
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input submission times TSV")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output Time Synchronization Score TSV")
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
    data = dict()
    for row_num, row in enumerate(infile):
        parts = [v.strip() for v in row.split('\t')]
        if row_num == 0:
            data[None] = parts
        else:
            if parts[0] in data:
                raise ValueError("Duplicate student: %s" % parts[0])
            times = [', '.join(parts[i].split(', ')[1:]).strip() for i in range(1, len(data[None]))]
            data[parts[0]] = sorted(parse_ed_timestamp(s) for s in times if s != '')

    # calculate Time Synchronization Scores
    students = sorted(set(data.keys())-{None})
    scores = list() # list of (score, student1, student2) tuples (for easy sorting)
    for si_ind in range(len(students)-1):
        si = students[si_ind]; si_times = data[si]
        for sj_ind in range(si_ind+1, len(students)):
            sj = students[sj_ind]; sj_times = data[sj]

            # if either student didn't submit any answers, score is infinity
            if len(si_times) == 0 or len(sj_times) == 0:
                scores.append((float('inf'), si, sj)); continue

            # right now, I just do a naive all-by-all comparison for each time of student i to find the closest time from student j
            # I can speed this up by merging the sorted lists of times and doing a local search for the closest time
            score = 0
            for ti in si_times:
                score += min((ti-tj).total_seconds()**2 for tj in sj_times)
            for tj in sj_times:
                score += min((ti-tj).total_seconds()**2 for ti in si_times)
            score /= (len(si_times) + len(sj_times)) # normalize by how many time comparisons we used
            scores.append((score, si, sj))

    # sort in ascending order of score (0 is very synchronized) and output
    scores.sort()
    outfile.write('Student 1\tStudent 2\tTime Synchronization Score\n')
    for score, si, sj in scores:
        outfile.write('%s\t%s\t%s\n' % (si, sj, score))
    infile.close(); outfile.close()
