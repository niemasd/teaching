#!/usr/bin/env python3
'''
Given a PrairieLearn Points CSV and an exported Canvas gradebook CSV, create a CSV that can be imported into Canvas
Niema Moshiri 2024
'''
from csv import reader,writer
from os.path import isfile
from sys import stderr

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--canvas_gradebook', required=True, type=str, help="Exported Canvas Gradebook (CSV)")
    parser.add_argument('-cc', '--canvas_column', required=True, type=int, help="Column of assignment in exported Canvas Gradebook (0-based indexing)")
    parser.add_argument('-q', '--pl_points', required=True, type=str, help="PrairieLearn Points (CSV)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output file to be imported into Canvas")
    parser.add_argument('-m', '--mapping', required=False, type=str, default=None, help="Manual PrairieLearn to Canvas mapping (TSV, col0=PrairieLearn, col1=Canvas)")
    args = parser.parse_args()
    if not isfile(args.canvas_gradebook):
        raise ValueError("File not found: %s" % args.canvas_gradebook)
    if args.canvas_column < 0:
        raise ValueError("Canvas column must be non-negative")
    if not isfile(args.pl_points):
        raise ValueError("File not found: %s" % args.pl_points)
    if args.output == 'stdout':
        from sys import stdout; args.output = stdout
    else:
        args.output = open(args.output, 'w')
    if args.mapping is None:
        pl2canvas = dict(); canvas2pl = dict()
    else:
        if not isfile(args.mapping):
            raise ValueError("File not found: %s" % args.mapping)
        lines = [[v.strip() for v in l.split('\t')] for l in open(args.mapping) if len(l.strip()) != 0]
        pl2canvas = {l[0]:l[1] for l in lines}; canvas2pl = {l[1]:l[0] for l in lines}
        if len(lines) != len(pl2canvas) or len(lines) != len(canvas2pl):
            raise ValueError("PrairieLearn to Canvas mapping file had duplicate items")

    # parse PrairieLearn Points
    quiz_score = dict()
    for row in reader(open(args.pl_points)):
        email = row[0].encode('ascii', 'ignore').decode().strip().lower()
        if email in {'', 'uid'}:
            continue # skip header lines
        score = float(row[2])
        uname = email.split('@')[0] # use usernames as keys instead of emails
        if uname not in quiz_score or score > quiz_score[uname]:
            quiz_score[uname] = score

    # parse exported Canvas gradebook
    out_csv = writer(args.output)
    for row in reader(open(args.canvas_gradebook)):
        if args.canvas_column >= len(row):
            raise ValueError("Canvas gradebook column out-of-bounds: %s" % args.canvas_column)
        student = row[0].strip()
        ID = row[1].strip()
        sis_user_ID = row[2].strip()
        sis_login_ID = row[3].strip().split('@')[0]
        section = row[4].strip()
        assignment = row[args.canvas_column].strip()
        if student == 'Student' and ID == 'ID' and sis_user_ID == 'SIS User ID' and sis_login_ID == 'SIS Login ID' and section == 'Section':
            out_csv.writerow([student, ID, sis_user_ID, sis_login_ID, section, assignment]) # write header
        elif 'Points Possible' in student or 'Student, Test' in student: # skip dummy rows
            pass
        else:
            curr_score = None
            if sis_login_ID in quiz_score:
                curr_score = quiz_score[sis_login_ID]
            if sis_login_ID in canvas2pl:
                tmp_s = canvas2pl[sis_login_ID].split('@')[0]
                if tmp_s in quiz_score:
                    if curr_score is None:
                        curr_score = quiz_score[tmp_s]
                    else:
                        curr_score = max(curr_score, quiz_score[tmp_s])
            if curr_score is None:
                stderr.write("CANVAS STUDENT NOT FOUND IN PRAIRIELEARN: %s\n" % sis_login_ID); curr_score = 0
            out_csv.writerow([student, ID, sis_user_ID, sis_login_ID, section, str(curr_score)])
    args.output.close()
