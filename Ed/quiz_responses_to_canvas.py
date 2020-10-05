#!/usr/bin/env python3
'''
Given an Ed Quiz Response CSV and an exported Canvas gradebook CSV, create a CSV that can be imported into Canvas
Niema Moshiri 2020
'''
from csv import reader,writer
from os.path import isfile
from sys import stderr
#from xlrd import open_workbook

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--canvas_gradebook', required=True, type=str, help="Exported Canvas Gradebook (CSV)")
    parser.add_argument('-cc', '--canvas_column', required=True, type=int, help="Column of assignment in exported Canvas Gradebook (0-based indexing)")
    parser.add_argument('-q', '--ed_quiz_responses', required=True, type=str, help="Ed Quiz Responses (CSV)")
    parser.add_argument('-qc', '--ed_quiz_columns', required=True, type=str, help="Column(s) of Ed Quiz Responses for each graded question (0-based indexing)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output file to be imported into Canvas")
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
        email = row[1].strip()
        if email == 'email':
            continue # skip header line
        score = 0
        for col in ed_columns:
            if col >= len(row):
                raise ValueError("Ed column out-of-bounds: %d" % col)
            score += int(row[col])
        quiz_score[email.split('@')[0]] = score # use usernames as keys instead of emails

    # parse exported Canvas gradebook
    out_csv = writer(args.output)
    for row in reader(open(args.canvas_gradebook)):
        if args.canvas_column >= len(row):
            raise ValueError("Canvas gradebook column out-of-bounds: %s" % args.canvas_column)
        student = row[0].strip()
        ID = row[1].strip()
        sis_user_ID = row[2].strip()
        sis_login_ID = row[3].strip()
        section = row[4].strip()
        assignment = row[args.canvas_column].strip()
        if student == 'Student' and ID == 'ID' and sis_user_ID == 'SIS User ID' and sis_login_ID == 'SIS Login ID' and section == 'Section':
            out_csv.writerow([student, ID, sis_user_ID, sis_login_ID, section, assignment]) # write header
        elif 'Points Possible' in student or 'Student, Test' in student: # skip dummy rows
            pass
        else:
            if sis_login_ID in quiz_score:
                out_csv.writerow([student, ID, sis_user_ID, sis_login_ID, section, str(quiz_score[sis_login_ID])])
            else:
                stderr.write("CANVAS STUDENT NOT FOUND IN ED: %s\n" % sis_login_ID)
    args.output.close()
