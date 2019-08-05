#!/usr/bin/env python3
'''
Grade all submissions of a specified PA
Niema Moshiri 2019
'''
from common import clone_repos
from datetime import datetime
from os import chdir,getcwd
from os.path import abspath,isdir
from subprocess import check_output,DEVNULL
from sys import stderr,stdout

def parse_args():
    '''
    Parses args and returns [student_list, github_group_url, repo_prefix, script, deadline, submission_message, outfile]
    '''
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--students', required=True, type=str, help="Students List (list of GitHub usernames)")
    parser.add_argument('-g', '--group', required=True, type=str, help="GitHub Group")
    parser.add_argument('-p', '--prefix', required=True, type=str, help="Repository Name Prefix")
    parser.add_argument('-gs', '--script', required=True, type=str, help="Grading Script (usage must be ./<script> <repo> and must print just point number to STDOUT)")
    parser.add_argument('-d', '--deadline', required=True, type=str, help="Deadline (MM/DD/YYYY HH:MM ±HHMM)")
    parser.add_argument('-d1', '--date1', required=False, type=str, default='01/01/1900 00:00 +0000', help="Front Cutoff Date (grade assignments after this) (MM/DD/YYYY HH:MM ±HHMM)")
    parser.add_argument('-m', '--message', required=False, type=str, default=None, help="Submission Commit Message")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose")
    parser.add_argument('-it', '--iterations', required=False, type=int, default=1, help="Number of times to try running grading script")
    args = parser.parse_args()
    global VERBOSE; VERBOSE = args.verbose
    global ITER; ITER = args.iterations
    students = [l.strip() for l in open(args.students)]
    group = "https://github.com/%s" % args.group
    script = abspath(args.script)
    deadline = datetime.strptime(args.deadline, "%m/%d/%Y %H:%M %z")
    date1 = datetime.strptime(args.date1, "%m/%d/%Y %H:%M %z")
    if args.output == 'stdout':
        outfile = stdout
    else:
        outfile = open(args.output,'w')
    if VERBOSE:
        print("Reading GitHub accounts from file: %s" % args.students, file=stderr)
        print("GitHub Group URL: %s" % group, file=stderr)
        print("Repo Prefix: %s" % args.prefix, file=stderr)
        print("Grading Script: %s" % script, file=stderr)
        print("Date 1: %s" % args.date1, file=stderr)
        print("Deadline: %s" % args.deadline, file=stderr)
        print("Submission Commit Message: %s" % args.message, file=stderr)
        print("Output File: %s" % args.output, file=stderr); stderr.flush()
    return students, group, args.prefix, script, date1, deadline, args.message, outfile

# main function: grade all repos
if __name__ == "__main__":
    # set up
    orig_dir = getcwd()
    students,group,prefix,script,date1,deadline,message,outfile = parse_args()
    repos = ['%s-%s' % (prefix,student) for student in students]
    repo_urls = ['%s/%s.git' % (group,repo) for repo in repos]

    # grade student repos
    clone_repos(repo_urls, deadline=deadline, date1=date1, message=message, verbose=VERBOSE); chdir(orig_dir)
    for i in range(len(students)):
        student = students[i]; repo = repos[i]
        if not isdir(repo):
            outfile.write("%s,0\n" % account); outfile.flush(); continue
        if VERBOSE:
            print("Grading submission for: %s" % student, file=stderr); stderr.flush()
        score = 0
        for _ in range(ITER):
            try:
                score = float(check_output([script,repo]).decode())
            except:
                pass
            if score > 0:
                break
        outfile.write("%s,%s\n" % (account,str(score))); outfile.flush()
    outfile.close()
