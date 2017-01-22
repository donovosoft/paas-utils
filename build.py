#!/usr/bin/python

import sys
import argparse
import json
from git import Repo
from subprocess import call

class Deployer(object):

    def read_info(self, app_name):
    	with open(app_name+'/package.json') as data:
    		myconfig = json.load(data)
    		self.app_version = myconfig.version
    		self.app_name = myconfig.app_name

    def clone_repo(self, repo):
    	Repo.clone_from(repo, '.')

    def build_docker(self):
    	call(['cd',self.app_name])
    	call(['docker', 'build', '.'])


def get_parser():
    parser = argparse.ArgumentParser(description='doNovosoft PAAS build')
    parser.add_argument('-n', '--name', help='Name of the application', required=True)
    parser.add_argument('-r', '--repo', help='Repository end point', required=True)
    parser.add_argument('-u', '--user', help='Username for registry', required=False)
    parser.add_argument('-p', '--password', help='Password for registry', required=False)
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    deploy = Deployer()
    deploy.clone_repo(args.repo)
    deploy.read_info(args.name)
    deploy.build_docker()


if __name__ == '__main__':
    main()
