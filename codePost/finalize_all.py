#!/usr/bin/env python3.7
'''
Finalize all codePost assignment submissions
Niema Moshiri 2019
'''
import codepost
GRADER = "niemamoshiri@gmail.com" # all finalized assignments must have a "grader"

# main function
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--course_id', required=True, type=int, help="codePost Course ID")
    args = parser.parse_args()

    # finalize all assignments using codePost API
    codepost_config = codepost.util.config.read_config_file()
    print("Loading codePost course (%d)..." % args.course_id, end=' ')
    while True:
        try:
            course = codepost.course.retrieve(id=args.course_id)
            break
        except Exception as e:
            pass
    print("done")
    for i,a in enumerate(course.assignments):
        print("Finalizing assignment %d of %d..." % (i+1, len(course.assignments)), end='\r')
        while True:
            try:
                subs = codepost.assignment.list_submissions(id=a.id)
                break
            except Exception as e:
                pass
        for sub in subs:
            if not sub.isFinalized:
                sub.isFinalized = True
                while True:
                    try:
                        sub.save()
                        break
                    except Exception as e:
                        pass
    print("Finalized %d assignments successfully" % len(course.assignments))
