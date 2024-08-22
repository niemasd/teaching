#! /usr/bin/env python3
'''
Run a Python unittest / Pytest grading script (test.py) in PrairieLearn. Assumes the following folder structure:

/grade/results/results.json             # test output formatted for PrairieLearn
/grade/serverFilesCourse/run_test.py    # this script
/grade/student/                         # folder containing student files to grade
/grade/tests/test*.py                   # Python unittest / Pytest scripts to run

https://prairielearn.readthedocs.io/en/latest/externalGrading/
'''

# imports
from pathlib import Path

# run grader
if __name__ == "__main__":
    # determine and check paths
    GRADE_DIR = Path(__file__).parent.parent
    RESULTS_DIR = GRADE_DIR / 'results'
    STUDENT_DIR = GRADE_DIR / 'student'
    TESTS_DIR = GRADE_DIR / 'tests'
    for d in [GRADE_DIR, STUDENT_DIR, TESTS_DIR]:
        assert d.is_dir(), "Directory not found: %s" % d
    RESULTS_DIR.mkdir(exist_ok=True)

    # run tests
    for test_py in TESTS_DIR.glob('test*.py'):
        print(test_py) # TODO