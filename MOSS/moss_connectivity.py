#!/usr/bin/env python3
'''
Given a list of MOSS URLs, create a JSON of the links between pairs of students
Files given to MOSS should be in a folder structure "email_address/file"
Niema Moshiri 2019
'''
from json import dump
from urllib.request import urlopen

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="MOSS URLs (one per line)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File (JSON)")
    args = parser.parse_args()
    if args.input == 'stdin':
        from sys import stdin as infile
    else:
        infile = open(args.input)
    if args.output == 'stdout':
        from sys import stdout as outfile
    else:
        outfile = open(args.output,'w')

    # parse MOSS URLs
    links = dict() # links[email1][email2] is a list of URLs of matches between email1 and email2
    for url in infile:
        page = urlopen(url).read().decode()
        susp = [l.strip() for l in page.replace('\n','').replace('<TR>','\n').replace('</TABLE>','\n').splitlines() if '/match' in l]
        for link in susp:
            moss_url = link.split('</A>')[0].split('HREF')[1].split('"')[1].strip()
            email1 = link.split('</A>')[0].split('HREF')[1].split('>')[1].split('/')[0].strip()
            email2 = link.split('</A>')[1].split('HREF')[1].split('>')[1].split('/')[0].strip()
            if email1 not in links:
                links[email1] = dict()
            if email2 not in links[email1]:
                links[email1][email2] = list()
            if email2 not in links:
                links[email2] = dict()
            if email1 not in links[email2]:
                links[email2][email1] = list()
            links[email1][email2].append(moss_url)
            links[email2][email1].append(moss_url)
    dump(links,outfile)
