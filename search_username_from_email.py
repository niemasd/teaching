#!/usr/bin/env python3
'''
Search for a GitHub username from an email address
Niema Moshiri 2019
'''
from github import Github
MESSAGE_EMAIL    = "Enter query email address: "
MESSAGE_PASSWORD = "Enter administrator GitHub password: "
MESSAGE_USERNAME = "Enter administrator GitHub username: "

def parse_args():
    '''
    Parses args and returns [GitHub object, organization name, list of GitHub usernames, role]
    '''
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument('-u', '--username', required=False, type=str, default=None, help="Administrator GitHub Username")
    #parser.add_argument('-p', '--password', required=False, type=str, default=None, help="Administrator GitHub Password")
    parser.add_argument('-e', '--email', required=False, type=str, default=None, help="Query Email Address")
    args = parser.parse_args()
    if args.email is None:
        print(MESSAGE_EMAIL, end=''); args.email = input().strip()
    #if args.username is None:
    #    print(MESSAGE_USERNAME, end=''); args.username = input().strip()
    #if args.password is None:
    #    from getpass import getpass; args.password = getpass(MESSAGE_PASSWORD).strip()
    return args.email#Github(args.username, args.password), args.email

# main function: clone all repos
if __name__ == "__main__":
    #gh, email = parse_args()
    email = parse_args()
    gh = Github()
    users = [u.login for u in gh.search_users("%s in:email" % email)]
    print("Found %d possible result%s" % (len(users), {True:'', False:'s'}[len(users) == 1]))
    if len(users) != 0:
        print('\n'.join(('* %s' % u) for u in users))
