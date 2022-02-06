#!/usr/bin/env python3
'''
Given a Canvas Gradebook export CSV with just a single assignment column, change the points for all students whose emails are listed in a given TXT file by some amount.
Niema Moshiri 2022
'''
from csv import reader,writer
from os.path import isfile
from sys import stderr
#from xlrd import open_workbook

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--canvas_gradebook', required=True, type=str, help="Exported Canvas Gradebook (CSV)")
    parser.add_argument('-e', '--emails', required=True, type=str, help="Student Email List (TXT)")
    parser.add_argument('-a', '--amount', required=True, type=float, help="Amount to Change Scores (+ for increase, - for decrease)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output file to be imported into Canvas")
    args = parser.parse_args()
    if not isfile(args.canvas_gradebook):
        raise ValueError("File not found: %s" % args.canvas_gradebook)
    if not isfile(args.emails):
        raise ValueError("File not found: %s" % args.emails)
    if args.output == 'stdout':
        from sys import stdout; args.output = stdout
    else:
        args.output = open(args.output, 'w')

    # load emails
    f = open(args.emails); email_usernames = {l.split('@')[0].strip() for l in f}; f.close()

    # parse exported Canvas gradebook
    out_csv = writer(args.output)
    for row in reader(open(args.canvas_gradebook)):
        if len(row) != 6:
            raise ValueError("Canvas gradebook should have exactly 6 columns: Student, ID, SIS User ID, SIS Login ID, Section, and the assignment")
        student = row[0].strip()
        ID = row[1].strip()
        sis_user_ID = row[2].strip()
        sis_login_ID = row[3].strip().split('@')[0]
        section = row[4].strip()
        assignment = row[5].strip()
        if student == 'Student' and ID == 'ID' and sis_user_ID == 'SIS User ID' and sis_login_ID == 'SIS Login ID' and section == 'Section':
            out_csv.writerow([student, ID, sis_user_ID, sis_login_ID, section, assignment]) # write header
        elif 'Points Possible' in student or 'Student, Test' in student: # skip dummy rows
            pass
        elif sis_login_ID in email_usernames: # skip students I'm not updating
            out_csv.writerow([student, ID, sis_user_ID, sis_login_ID, section, str(float(assignment)+args.amount)])
    args.output.close()
