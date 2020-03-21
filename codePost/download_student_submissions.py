#!/usr/bin/env python3.7
'''
Download all student submissions for a given codePost assignment
Niema Moshiri 2019
'''
from os.path import isfile
from os import mkdir
from zipfile import ZipFile,ZIP_DEFLATED
import codepost

# main function
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--course_id', required=True, type=int, help="codePost Course ID")
    parser.add_argument('-a', '--assignment_name', required=True, type=str, help="codePost Assignment Name")
    parser.add_argument('-o', '--output', required=True, type=str, help="Output File (zip)")
    args = parser.parse_args()
    if not args.output.lower().endswith('.zip'):
        raise ValueError("Output file must be a zip file")
    if isfile(args.output):
        raise ValueError("Output file exists: %s" % args.output)

    # load codePost configuration
    codepost_config = codepost.util.config.read_config_file()

    # get codePost course
    print("Loading codePost course...", end=' ')
    while True:
        try:
            course = codepost.course.retrieve(id=args.course_id)
            break
        except Exception as e:
            pass
    print("done")

    # get codePost assignment
    print("Finding assignment (%s)..." % args.assignment_name, end=' ', flush=True)
    assignment = None
    for a in course.assignments:
        while True:
            try:
                curr = codepost.assignment.retrieve(id=a.id)
                break
            except:
                pass
        if curr.name.strip() == args.assignment_name.strip():
            assignment = curr; break
    if assignment is None:
        raise ValueError("Assignment not found: %s" % args.assignment_name)
    print("done")

    # get submissions list
    print("Getting list of submissions...", end=' ', flush=True)
    while True:
        try:
            subs = codepost.assignment.list_submissions(id=assignment.id)
            break
        except:
            pass
    print("done")

    # download submissions
    outzip = ZipFile(args.output, mode='w', compression=ZIP_DEFLATED)
    for sub_num,sub in enumerate(subs):
        print("Downloading submission %d of %d..." % (sub_num+1,len(subs)), end='\r', flush=True)
        sub_dir = ','.join(sub.students)
        for f in sub.files:
            while True:
                try:
                    curr_file = codepost.file.retrieve(id=f.id)
                    break
                except:
                    pass
            outzip.writestr("%s/%s" % (sub_dir, curr_file.name.strip()), curr_file.code)
    print("Successfully downloaded %d submissions" % len(subs))
