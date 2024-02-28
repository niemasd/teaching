#!/usr/bin/env python3
'''
Given an Ed Quiz Response CSV and an exported Canvas gradebook CSV, create a CSV that can be imported into Canvas
Niema Moshiri 2020
'''
from csv import reader,writer
from os.path import isfile
from sys import stderr

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--canvas_gradebook', required=True, type=str, help="Exported Canvas Gradebook (CSV)")
    parser.add_argument('-cc', '--canvas_column', required=True, type=int, help="Column of assignment in exported Canvas Gradebook (0-based indexing)")
    parser.add_argument('-q', '--ed_quiz_responses', required=True, type=str, help="Ed Quiz Responses (CSV)")
    parser.add_argument('-qc', '--ed_quiz_columns', required=True, type=str, help="Column(s) of Ed Quiz Responses for each graded question (0-based indexing)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output file to be imported into Canvas")
    parser.add_argument('-m', '--mapping', required=False, type=str, default=None, help="Manual Ed to Canvas mapping (TSV, col0=Ed, col1=Canvas)")
    args = parser.parse_args()
    if not isfile(args.canvas_gradebook):
        raise ValueError("File not found: %s" % args.canvas_gradebook)
    if args.canvas_column < 0:
        raise ValueError("Canvas column must be non-negative")
    if not isfile(args.ed_quiz_responses):
        raise ValueError("File not found: %s" % args.ed_quiz_responses)
    if args.output == 'stdout':
        from sys import stdout; args.output = stdout
    else:
        args.output = open(args.output, 'w')
    if args.mapping is None:
        ed2canvas = dict(); canvas2ed = dict()
    else:
        if not isfile(args.mapping):
            raise ValueError("File not found: %s" % args.mapping)
        lines = [[v.strip() for v in l.split('\t')] for l in open(args.mapping) if len(l.strip()) != 0]
        ed2canvas = {l[0]:l[1] for l in lines}; canvas2ed = {l[1]:l[0] for l in lines}
        if len(lines) != len(ed2canvas) or len(lines) != len(canvas2ed):
            raise ValueError("Ed to Canvas mapping file had duplicate items")

    # parse Ed columns
    ed_columns = list()
    try:
        for part in args.ed_quiz_columns.split(','):
            if '-' in part:
                a,b = part.split('-'); ed_columns += list(range(int(a),int(b)+1))
            else:
                ed_columns.append(int(part))
    except:
        raise ValueError("Invalid Ed columns selection: %s" % args.ed_quiz_columns)
    for col in ed_columns:
        if col < 0:
            raise ValueError("Ed columns must be non-negative")

    # parse Ed Quiz Response
    quiz_score = dict()
    for row in reader(open(args.ed_quiz_responses)):
        email = row[0].encode('ascii', 'ignore').decode().strip().lower()
        if email in {'', 'email', 'users', 'submissions'}:
            continue # skip header lines
        score = 0
        for col in ed_columns:
            if col >= len(row):
                raise ValueError("Ed column out-of-bounds: %d" % col)
            score += float(row[col])
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
            if sis_login_ID in quiz_score:
                curr_score = quiz_score[sis_login_ID]
            elif sis_login_ID in canvas2ed and canvas2ed[sis_login_ID].split('@')[0] in quiz_score:
                curr_score = quiz_score[canvas2ed[sis_login_ID].split('@')[0]]
            else:
                stderr.write("CANVAS STUDENT NOT FOUND IN ED: %s\n" % sis_login_ID); curr_score = 0
            out_csv.writerow([student, ID, sis_user_ID, sis_login_ID, section, str(curr_score)])
    args.output.close()
