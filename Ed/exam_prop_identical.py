#!/usr/bin/env python3
'''
Given multiple Ed "Quiz Responses" files, compute the proportion of identical responses between pairs of students
Niema Moshiri 2021
'''
from csv import reader,writer
from os.path import isfile
from sys import argv

if __name__ == "__main__":
    # check usage
    if len(argv) < 2 or argv[1].lower() in {'-h','-help','--help'}:
        print("USAGE: %s <responses_csv_1> [responses_csv_2] ..." % argv[0]); exit(1)

    # load student responses
    responses   = dict() # responses[email][filename][question_ID] = (points, response) tuple
    columns     = dict() # columns[filename] = list of (question_ID, response_index, correctness_index) tuples
    for fn in argv[1:]:
        if not isfile(fn):
            raise ValueError("File not found: %s" % fn)
        for row in reader(open(fn)):
            email = row[1].strip()
            if email == 'email':
                if fn not in columns:
                    tmp_response_index = dict()
                    tmp_points_index = dict()
                    for col in range(3, len(row)):
                        val = row[col].strip()
                        if val.endswith(' score'):
                            tmp_points_index[val.rstrip(' score').strip()] = col
                        else:
                            tmp_response_index[val] = col
                    columns[fn] = [(qid,tmp_response_index[qid],tmp_points_index[qid]) for qid in tmp_points_index]
                continue # skip header line
            if email not in responses:
                responses[email] = dict()
            if fn not in responses[email]:
                responses[email][fn] = dict()
            for qid, res_ind, pts_ind in columns[fn]:
                res = row[res_ind].strip()
                pts = int(row[pts_ind])            # 0 = incorrect, non-0 = correct
                if len(res) == 0:                  # response is empty string, so student didn't submit an answer
                    res = None
                responses[email][fn][qid] = (pts, res)

    # compare pairs of students
    emails = sorted(responses.keys())
    scores = list() # (score, email1, email2) tuples
    tot_num_qs = sum(len(columns[fn]) for fn in columns)
    for e1_ind in range(len(emails)-1):
        email1 = emails[e1_ind]
        for e2_ind in range(e1_ind+1, len(emails)):
            email2 = emails[e2_ind]; score = 0.
            for fn in columns:
                for qid, res_ind, cor_ind in columns[fn]:
                    pts1 = 0; res1 = None; pts2 = 0; res2 = None
                    if fn in responses[email1] and qid in responses[email1][fn]:
                        pts1, res1 = responses[email1][fn][qid]
                    if fn in responses[email2] and qid in responses[email2][fn]:
                        pts2, res2 = responses[email2][fn][qid]
                    if res1 == res2:
                        score += 1
            score /= tot_num_qs # normalize by number of questions
            scores.append((score, email1, email2))

    # print output
    scores.sort(reverse=True) # sort similarity scores in descending order
    print("Email 1,Email 2,Proportion Identical")
    for score, email1, email2 in scores:
            print("%s,%s,%f" % (email1, email2, score))
