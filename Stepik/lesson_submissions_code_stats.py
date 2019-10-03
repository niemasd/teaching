#!/usr/bin/env python3
'''
Given a Stepik lesson submission report, visualize and print some statistics about coding challenges
Niema Moshiri 2019
'''
from xlrd import open_workbook

# main function: grade all repos
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--submissions', required=True, type=str, help="Stepik Lesson Submission Report (XLSX)")
    args = parser.parse_args()

    # parse submission report
    subs_by_stepik_id = dict()
    subs = open_workbook(args.submissions).sheet_by_index(0)
    for rowx in range(subs.nrows):
        sub_id,step_id,user_id,last,first,attempt_time,sub_time,status,dataset,clue,reply,reply_clear,hint = subs.row_values(rowx)
        if sub_id == "submission_id":
            continue # header line
        step_id = int(float(step_id)); user_id = int(float(user_id)); reply = eval(reply)
        #sub_time = datetime.fromtimestamp(float(sub_time), timezone.utc)
        if 'code' not in reply:
            continue
        if user_id not in subs_by_stepik_id:
            subs_by_stepik_id[user_id] = dict()
        if step_id not in subs_by_stepik_id[user_id]:
            subs_by_stepik_id[user_id][step_id] = list()
        subs_by_stepik_id[user_id][step_id].append({'code':reply['code'], 'status':status, 'time':float(sub_time)})
    print(subs_by_stepik_id)
