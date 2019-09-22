#!/usr/bin/env python3
'''
Given a Stepik lesson submission report, for each student, export a PDF of their submissions (one per page)
Niema Moshiri 2019
'''
from datetime import datetime,timezone
from fpdf import FPDF
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
    pid_to_stepik = dict()
    for l in open(args.roster):
        last,first,email,pid,stepik,iclicker,grade = [v.strip() for v in l.strip().split('\t')]
        assert pid not in pid_to_stepik, "Duplicate PID: %s" % pid
        pid_to_stepik[pid] = int(stepik)
    stepik_to_pid = {pid_to_stepik[pid]:pid for pid in pid_to_stepik}
    passed = {pid:dict() for pid in pid_to_stepik}

    # parse submission report
    subs_by_pid = {pid:dict() for pid in pid_to_stepik}
    subs = open_workbook(args.submissions).sheet_by_index(0)
    for rowx in range(subs.nrows):
        #print(subs.row_values(rowx))
        sub_id,step_id,user_id,last,first,attempt_time,sub_time,status,dataset,clue,reply,reply_clear,hint = subs.row_values(rowx)
        if sub_id == "submission_id":
            continue # header line
        step_id = int(float(step_id)); user_id = int(float(user_id)); reply = eval(reply)
        sub_time = datetime.fromtimestamp(float(sub_time), timezone.utc)
        if user_id not in stepik_to_pid or status == 'wrong' or sub_time > deadline:
            continue
        if 'code' not in reply and 'answer' not in reply:
            continue
        pid = stepik_to_pid[user_id]
        passed[pid][step_id] = reply

    # output student grades
    f = open('%s/points.tsv' % args.outdir, 'w')
    for pid in passed:
        f.write('%s\t%s\n' % (pid,len(passed[pid])))
    f.close()

    # output student PDFs
    for pid in passed:
        pdf = FPDF(orientation='L')
        pdf.set_auto_page_break(True)
        for step_id in sorted(passed[pid].keys()):
            if 'code' not in passed[pid][step_id]:
                continue
            pdf.add_page()
            pdf.set_font('Courier','B',16)
            pdf.cell(60,10,"PROBLEM CODE START",'C'); pdf.ln()
            pdf.set_font('Courier','',16)
            for l in passed[pid][step_id]['code'].splitlines():
                pdf.cell(60,10,l,'C'); pdf.ln()
            pdf.set_font('Courier','B',16)
            pdf.cell(60,10,"PROBLEM CODE END",'C')
        pdf.output('%s/%s.pdf' % (args.outdir, pid))
