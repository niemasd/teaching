#!/usr/bin/env python3
'''
Given iClicker participation points, create a codePost assignment with points (1 or 0) via codePost API
Niema Moshiri 2019
'''
import codepost
GRADER = "niemamoshiri@gmail.com" # all finalized assignments must have a "grader"
CODEPOST_ATTEMPTS = 10 # try calling codePost API this many times (in case of temporary server error)

# main function
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', '--roster', required=True, type=str, help="Roster (TSV) (Last, First, Email, PID, Stepik, iClicker, Grade ID)")
    parser.add_argument('-i', '--iclicker', required=True, type=str, help="iClicker Report (CSV) (Last, First, PID, iClicker, Points)")
    parser.add_argument('-c', '--course_id', required=True, type=int, help="codePost Course ID")
    parser.add_argument('-a', '--assignment_name', required=True, type=str, help="codePost Assignment Name")
    args = parser.parse_args()

    # parse roster
    print("Parsing roster: %s" % args.roster)
    email_to_iclicker = dict()
    for l in open(args.roster):
        if l.startswith("Last Name\t"):
            continue
        last,first,email,pid,stepik,iclicker = [v.strip() for v in l.strip().split('\t')][:6]
        assert email == '' or email not in email_to_iclicker, "Duplicate Email: %s" % email
        email_to_iclicker[email] = iclicker
    iclicker_to_email = {email_to_iclicker[email]:email for email in email_to_iclicker}
    if '' in iclicker_to_email:
        del iclicker_to_email[''] # delete dummy missing value
    points = {email:0 for email in email_to_iclicker}
    print("Loaded %d students from roster." % len(iclicker_to_email))

    # parse iClicker report
    print("Parsing iClicker participation report: %s" % args.iclicker)
    for l in open(args.iclicker):
        if l.startswith('Last Name'):
            continue
        try:
            last,first,pid,iclicker,p = [v.strip().replace('"','').replace("'",'') for v in l.split(',')]
        except:
            assert False, "Failed to parse line:\n%s" % l
        if len(iclicker) != 0 and iclicker[0] == '#':
            iclicker = iclicker[1:]
        if iclicker in iclicker_to_email and points[iclicker_to_email[iclicker]] == 0:
            try:
                points[iclicker_to_email[iclicker]] = int(float(p))
            except:
                pass # points are 0 by default
    print("Loaded iClicker participation points.")

    # load codePost configuration and course
    codepost_config = codepost.util.config.read_config_file()

    # create codePost assignment and upload submissions
    print("Creating new codePost assignment (%s)..." % args.assignment_name, end=' ')
    for _ in range(CODEPOST_ATTEMPTS):
        try:
            codepost_assignment = codepost.assignment.create(name=args.assignment_name, points=1, course=args.course_id)
            break
        except Exception as e:
            pass
        raise RuntimeError("Failed to create codePost assignment:\n%s" % str(e))
    print("done")
    print("Uploading %d student points to codePost..." % len(points))
    for student_num,email in enumerate(points.keys()):
        print("Student %d of %d..." % (student_num+1, len(points)), end='\r')
        for _ in range(CODEPOST_ATTEMPTS):
            try:
                codepost_sub = codepost.submission.create(assignment=codepost_assignment.id, students=[email], isFinalized=True, grader=GRADER)
                break
            except Exception as e:
                pass
            raise RuntimeError("Failed to create codePost submission:\n%s" % str(e))
        for _ in range(CODEPOST_ATTEMPTS):
            try:
                grade_file = codepost.file.create(name="grade.txt", code="Grade: %d/1"%(points[email]), extension='txt', submission=codepost_sub.id)
                break
            except Exception as e:
                pass
            raise RuntimeError("Failed to create grade file:\n%s" % str(e))
        point_delta = 1 - points[email] # codePost currently assumes subtractive points; update this when they integrate additive
        for _ in range(CODEPOST_ATTEMPTS):
            try:
                grade_comment = codepost.comment.create(text='points', startChar=0, endChar=0, startLine=0, endLine=0, file=grade_file.id, pointDelta=point_delta, rubricComment=None)
                break
            except:
                pass
            raise RuntimeError("Failed to create comment with score:\n%s" % str(e))
    print("Successfully uploaded %d student points" % len(points))
