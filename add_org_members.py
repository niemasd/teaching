#!/usr/bin/env python3
'''
Add a list of GitHub usernames to be members of a GitHub organization
Niema Moshiri 2019
'''
from github import Github
MESSAGE_LIST     = "Enter list of GitHub member usernames (comma-separated): "
MESSAGE_ORG      = "Enter GitHub organization: "
MESSAGE_PASSWORD = "Enter administrator GitHub password: "
MESSAGE_USERNAME = "Enter administrator GitHub username: "
VALID_ROLES = {'member', 'admin'}

def parse_args():
    '''
    Parses args and returns [GitHub object, organization name, list of GitHub usernames, role]
    '''
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--username', required=False, type=str, default=None, help="Administrator GitHub Username")
    parser.add_argument('-p', '--password', required=False, type=str, default=None, help="Administrator GitHub Password")
    parser.add_argument('-l', '--list', required=False, type=argparse.FileType('r', encoding='UTF-8'), default=None, help="List of GitHub Member Usernames (one per line)")
    parser.add_argument('-o', '--organization', required=False, type=str, default=None, help="GitHub Organization")
    parser.add_argument('-r', '--role', required=False, type=str, default='member', help="Organization Role")
    args = parser.parse_args()
    if args.role not in VALID_ROLES:
        raise ValueError("Invalid organization role: %s\nValid options: %s" % (args.role, ', '.join(sorted(VALID_ROLES))))
    if args.organization is None:
        print(MESSAGE_ORG, end=''); args.organization = input().strip()
    if args.list is None:
        print(MESSAGE_LIST, end=''); args.list = [e.strip() for e in input().strip().split(',')]
    else:
        args.list = [l.strip() for l in args.list]
    if args.username is None:
        print(MESSAGE_USERNAME, end=''); args.username = input().strip()
    if args.password is None:
        from getpass import getpass; args.password = getpass(MESSAGE_PASSWORD).strip()
    return Github(args.username, args.password), args.organization, args.list, args.role

# main function: clone all repos
if __name__ == "__main__":
    gh, org_name, users, role = parse_args(); org = gh.get_organization(org_name)
    for u in users:
        try:
            u_obj = gh.get_user(u)
        except:
            raise RuntimeError("Unable to get user: %s" % u)
        org.add_to_members(u_obj, role=role)
