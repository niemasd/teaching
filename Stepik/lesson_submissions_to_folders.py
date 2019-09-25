#!/usr/bin/env python3
'''
Given a Stepik lesson submission report, for each student, output a folder with code files (uploadable to codePost)
Niema Moshiri 2019
'''
from datetime import datetime,timezone
from os.path import isdir
from os import mkdir
from xlrd import open_workbook

# main function: grade all repos
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', '--roster', required=True, type=str, help="Roster (TSV) (Last, First, Email, PID, Stepik, iClicker, Grade ID)")
    parser.add_argument('-s', '--submissions', required=True, type=str, help="Stepik Lesson Submission Report (XLSX)")
    parser.add_argument('-d', '--deadline', required=True, help="Deadline (MM/DD/YYYY HH:MM ±HHMM)")
    parser.add_argument('-o', '--outdir', required=True, type=str, help="Output Directory")
    args = parser.parse_args()
    deadline = datetime.strptime(args.deadline, "%m/%d/%Y %H:%M %z")
    assert not isdir(args.outdir)
    mkdir(args.outdir)

    # parse roster
    email_to_stepik = dict()
    for l in open(args.roster):
        if l.startswith("Last Name\t"):
            continue
        last,first,email,pid,stepik,iclicker = [v.strip() for v in l.strip().split('\t')]
        assert email not in email_to_stepik, "Duplicate Email: %s" % email
        email_to_stepik[email] = int(stepik)
    stepik_to_email = {email_to_stepik[email]:email for email in email_to_stepik}
    passed = {email:dict() for email in email_to_stepik}

    # parse submission report
    subs_by_email = {email:dict() for email in email_to_stepik}
    subs = open_workbook(args.submissions).sheet_by_index(0)
    for rowx in range(subs.nrows):
        sub_id,step_id,user_id,last,first,attempt_time,sub_time,status,dataset,clue,reply,reply_clear,hint = subs.row_values(rowx)
        if sub_id == "submission_id":
            continue # header line
        step_id = int(float(step_id)); user_id = int(float(user_id)); reply = eval(reply)
        sub_time = datetime.fromtimestamp(float(sub_time), timezone.utc)
        if user_id not in stepik_to_email or status == 'wrong' or sub_time > deadline:
            continue
        if 'code' not in reply and 'answer' not in reply:
            continue
        email = stepik_to_email[user_id]
        passed[email][step_id] = reply

    # output student grades
    f = open('%s/points.tsv' % args.outdir, 'w')
    for email in passed:
        f.write('%s\t%s\n' % (email,len(passed[email])))
    f.close()

    # output student code
    for email in passed:
        if len([step_id for step_id in passed[email] if 'code' in passed[email][step_id]]) == 0:
            continue
        mkdir("%s/%s" % (args.outdir, email))
        for step_id in sorted(passed[email].keys()):
            if 'code' in passed[email][step_id]:
                f = open("%s/%s/%d.txt" % (args.outdir, email, step_id), 'w')
                f.write(passed[email][step_id]['code'])
                f.close()
