#!/usr/bin/env python3
'''
Given a list of MOSS URLs, create a JSON of the links between pairs of students
Files given to MOSS should be in a folder structure "email_address/file"
Niema Moshiri 2019
'''
from bs4 import BeautifulSoup
from json import dump
from sys import stderr
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
    urls = [l.strip() for l in infile.read().strip().splitlines()]
    for url_num,url in enumerate(urls):
        stderr.write("Parsing MOSS report %d of %d...\r" % (url_num+1, len(urls)))
        bs = BeautifulSoup(urlopen(url).read().decode(), "lxml")
        for row in bs.findAll('tr'):
            cols = row.findAll('td')
            if len(cols) != 3:
                continue
            try:
                moss_url = cols[0].find_all('a', href=True)[0]['href']
            except:
                stderr.write("Failed to parse row: %s" % row); continue
            email1 = cols[0].find_all('a', href=True)[0].text.split('/')[1]
            email2 = cols[1].find_all('a', href=True)[0].text.split('/')[1]
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
    stderr.write("Successfully parsed %d MOSS reports\n" % len(urls))
    stderr.write("Dumping results (%s)... " % args.output)
    dump(links,outfile)
    stderr.write("done\n")
