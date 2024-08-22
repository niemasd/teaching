#! /usr/bin/env python3
'''
Run a Python unittest / Pytest grading script (test.py) in PrairieLearn.
Tests will be run in alphabetical order of filename followed by class name followed by function name.
Assumes the following folder structure:

/grade/results/results.json             # test output formatted for PrairieLearn
/grade/serverFilesCourse/run_test.py    # this script
/grade/student/                         # folder containing student files to grade
/grade/tests/test*.py                   # Python unittest / Pytest scripts to run

https://prairielearn.readthedocs.io/en/latest/externalGrading/
'''

# imports
from inspect import isclass
from json import dump as jdump
from os import chdir
from pathlib import Path
from runpy import run_path
from unittest import TestCase

# constants
ZERO_THRESH = 0.000001

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
    results = list(); num_tests = 0 # `results` is a list of (name str, points possible int/float, points earned int/float, feedback str) tuples
    for test_py in sorted(TESTS_DIR.glob('test*.py')):
        for k, v in sorted(run_path(test_py).items()):
            # instantiate TestCase-derived class
            if not (isclass(v) and v != TestCase and issubclass(v, TestCase)):
                continue # only look at subclasses of TestCase
            test_obj = v()

            # iterate over members of TestCase-derived object
            for v_member in sorted(dir(test_obj)):
                # prepare for running test
                if not v_member.startswith('test'):
                    continue # only look at methods starting with 'test'
                num_tests += 1; test_func = getattr(test_obj, v_member); test_name = "Test %d" % num_tests; test_points = 1; test_feedback = "Success"

                # parse test name and points from docstring (if available)
                if test_func.__doc__ is not None:
                    for part in test_func.__doc__.split('#'):
                        tmp = part.replace(' ','')
                        if tmp.startswith('name('):
                            test_name = part.split('(')[1].split(')')[0].strip()
                        elif tmp.startswith('score('):
                            test_points = float(part.split('(')[1].split(')')[0])
                            if abs(test_points - int(test_points)) < ZERO_THRESH:
                                test_points = int(test_points)

                # run test
                chdir(STUDENT_DIR); student_points = test_points
                try:
                    test_func()
                except Exception as e:
                    student_points = 0; test_feedback = str(e).strip()
                results.append((test_name, test_points, student_points, test_feedback))

    # calculate and write results
    assert len(results) != 0, "No tests detected in path: %s" % TESTS_DIR
    results_json = {
        'gradable': True,
        'tests': list()
    }
    total_points_possible = 0; total_points_student = 0
    for test_name, test_points, student_points, test_feedback in results:
        total_points_possible += test_points; total_points_student += student_points
        results_json['tests'].append({
            'name': test_name,
            'points': student_points,
            'max_points': test_points,
            'message': test_feedback,
        })
    results_json["score"] = total_points_student / total_points_possible
    with open(RESULTS_DIR / 'results.json', 'w') as results_f:
        jdump(results_json, results_f)