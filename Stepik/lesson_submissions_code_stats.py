#!/usr/bin/env python3
'''
Given a Stepik lesson submission report, visualize and print some statistics about coding challenges
Niema Moshiri 2019
'''
from os.path import isdir
from os import mkdir
from seaborn import boxenplot
from xlrd import open_workbook
import matplotlib.pyplot as plt

# main function: grade all repos
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--submissions', required=True, type=str, help="Stepik Lesson Submission Report (XLSX)")
    args = parser.parse_args()

    # parse submission report
    subs = dict() # subs[step_id][user_id] = list of submission attempts (dicts)
    report = open_workbook(args.submissions).sheet_by_index(0)
    for rowx in range(report.nrows):
        sub_id,step_id,user_id,last,first,attempt_time,sub_time,status,dataset,clue,reply,reply_clear,hint = report.row_values(rowx)
        if sub_id == "submission_id":
            continue # header line
        step_id = int(float(step_id)); user_id = int(float(user_id)); reply = eval(reply)
        #sub_time = datetime.fromtimestamp(float(sub_time), timezone.utc)
        if 'code' not in reply:
            continue
        if step_id not in subs:
            subs[step_id] = dict()
        if user_id not in subs[step_id]:
            subs[step_id][user_id] = list()
        subs[step_id][user_id].append({'code':reply['code'], 'status':status, 'time':float(sub_time)})

    # number of attempts until success
    x = list(); y = list()
    for step_id in subs:
        for user_id in subs[step_id]:
            num_subs = 0; passed = False
            for sub in subs[step_id][user_id]:
                num_subs += 1
                if sub['status'].strip().lower() == 'correct':
                    passed = True; break
            if passed:
                x.append(step_id); y.append(num_subs)
    fig = plt.figure()
    ax = boxenplot(x=x, y=y)
    plt.title("Attempts Until Success")
    plt.ylabel("Number of Attempts")
    plt.ylim(ymin=0,ymax=20)
    fig.savefig('num_attempts_until_success.pdf')

    # time until success
    x = list(); y = list()
    for step_id in subs:
        for user_id in subs[step_id]:
            t_first = subs[step_id][user_id][0]['time']; t_last = None
            for sub in subs[step_id][user_id]:
                if sub['status'].strip().lower() == 'correct':
                    t_last = sub['time']; break
            if t_last is not None:
                x.append(step_id); y.append((t_last-t_first)/1440)
    fig = plt.figure()
    ax = boxenplot(x=x, y=y)
    plt.title("Time Until Success")
    plt.ylabel("Time (Hours)")
    plt.ylim(ymin=0,ymax=5)
    fig.savefig('time_until_success.pdf')
