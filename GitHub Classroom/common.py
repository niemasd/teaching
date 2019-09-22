#!/usr/bin/env python3
'''
Common functions needed by these tools
Niema Moshiri 2019
'''
from datetime import datetime
from os import chdir,getcwd
from os.path import isdir
from subprocess import check_output,DEVNULL
from sys import stderr

def clone_repos(urls, deadline=None, date1=None, message=None, verbose=False):
    '''
    Clone all repos made between `date1` and `deadline` with a specific message and return a list with True for all successful ones and False for all failed ones
    '''
    out = list(); orig_dir = getcwd()
    if verbose:
        print("Attempting to clone %d git repos..." % len(urls), file=stderr); stderr.flush()
    for i,url in enumerate(urls):
        repo = url.split('/')[-1].rstrip('.git')
        if verbose:
            print("Cloning repo %d of %d..." % (i+1,len(urls)), file=stderr, end='\r'); stderr.flush()
        try:
            if isdir(repo):
                chdir(repo); check_output(['git','pull'], stderr=DEVNULL)
            else:
                check_output(['git','clone',url], stderr=DEVNULL); chdir(repo)
            commits = [line.strip().split('\t') for line in check_output(['git','log','--pretty="format:\%s\t\%ad\t\%H"'], stderr=DEVNULL).decode().replace('\\','').replace('"','').replace('format:','').splitlines()]
            commits = [(m,datetime.strptime(t, "%a %b %d %H:%M:%S %Y %z"),h) for m,t,h in commits]
            commits.sort(key=lambda x: x[1], reverse=True); submission_commit = None
            for m,t,h in commits:
                if (message is None or message.upper() in m.upper()) and (date1 is None or t >= date1) and (deadline is None or t <= deadline):
                    submission_commit = h; break
            if submission_commit is None:
                out.append(False); continue
            check_output(['git','reset','--hard',submission_commit])
            out.append(True)
        except:
            out.append(False)
        chdir(orig_dir)
    return out
