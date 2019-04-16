#!/usr/bin/env python3
'''
Grade all submissions of a specified PA
Niema Moshiri 2019
'''
import argparse
from datetime import datetime
from os import chdir,getcwd
from os.path import abspath
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
    parser.add_argument('-gs', '--script', required=True, type=str, help='Grading Script (usage must be ./<script> <repo> and must print just point number to STDOUT)')
    parser.add_argument('-d', '--deadline', required=True, type=str, help='Deadline (MM/DD/YY HH:MM)')
    parser.add_argument('-m', '--message', required=False, type=str, default=None, help="Submission Commit Message")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
    args = parser.parse_args()
    students = [l.strip() for l in open(args.students)]
    print("Reading GitHub accounts from file: %s" % args.students, file=stderr)
    group = "https://github.com/%s" % args.group
    print("GitHub Group URL: %s" % group, file=stderr)
    print("Repo Prefix: %s" % args.prefix, file=stderr)
    script = abspath(args.script)
    print("Grading Script: %s" % script, file=stderr)
    deadline = datetime.strptime(args.deadline, "%m/%d/%y %H:%M")
    print("Deadline: %s" % args.deadline, file=stderr)
    print("Submission Commit Message: %s" % args.message, file=stderr)
    print("Output File: %s" % args.output, file=stderr)
    if args.output == 'stdout':
        outfile = stdout
    else:
        outfile = open(args.output,'w')
    return students, group, args.prefix, script, deadline, args.message, outfile

# main function: grade all repos
if __name__ == "__main__":
    # set up
    orig_dir = getcwd()
    students,group,prefix,script,deadline,message,outfile = parse_args()

    # grade student repos
    print("Grading student repositories...", file=stderr)
    for account in students:
        # prep things
        chdir(orig_dir)
        repo = "%s-%s" % (prefix,account)
        repo_url = "%s/%s.git" % (group,repo)

        # try to clone
        try:
            check_output(['git','clone',repo_url], stderr=DEVNULL)
        except:
            outfile.write("%s,0\n" % account); print("Failed to clone: %s" % repo_url, file=stderr); continue

        # revert to last commit before deadline
        chdir(repo)
        commits = [line.strip().split('\t') for line in check_output(['git','log','--pretty="format:\%s\t\%at\t\%H"'], stderr=DEVNULL).decode().replace('\\','').replace('"','').replace('format:','').splitlines()]
        commits.sort(key=lambda x: x[1], reverse=True); submission_commit = None
        for m,t,h in commits:
            if (message is None or args.message.upper() in m.upper()) and datetime.fromtimestamp(int(t)) < deadline:
                submission_commit = h; break
        if submission_commit is None:
            outfile.write("%s,0\n" % account); print("No on-time submission for: %s" % account, file=stderr); continue
        check_output(['git','reset','--hard',submission_commit]); chdir(orig_dir)

        # grade submission
        print("Grading submission for: %s" % account, file=stderr)
        try:
            score = float(check_output(['python3',script,repo]).decode())
        except:
            score = 0
        print("%s,%f\n" % (account,score))
