#!/usr/bin/python
import docker
import sys
import argparse
import json
from pprint import pprint
from git import Repo
from subprocess import call

class Deployer(object):

    def __init__(self):
		self.app_name = None
		self.app_version = None

    def read_info(self, app_name):
    	with open(app_name+'/package.json') as data:
    		myconfig = json.load(data)
    		self.app_version = myconfig["version"]
    		self.app_name = myconfig["name"]

    def clone_repo(self, repo, app_name):
    	Repo.clone_from(repo, app_name)

    def build_docker(self, user, passw):
    	client = docker.from_env()
    	dockerfile = self.app_name+'/'
    	tag = 'donovosoft/'+self.app_name
    	image = client.images.build(path=dockerfile, stream=False)
    	image.tag(tag, self.app_version)
    	client.login(username=user, password=passw)
    	for line in client.images.push('docker.io/'+tag, self.app_version, stream=True):
    		print line
    	print "Build OK"

def get_parser():
    parser = argparse.ArgumentParser(description='doNovosoft PAAS build')
    parser.add_argument('-n', '--name', help='Name of the application', required=True)
    parser.add_argument('-r', '--repo', help='Repository end point', required=True)
    parser.add_argument('-u', '--user', help='Username for registry', required=True)
    parser.add_argument('-p', '--password', help='Password for registry', required=False)
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    deploy = Deployer()
    deploy.clone_repo(args.repo, args.name)
    deploy.read_info(args.name)
    deploy.build_docker(args.user, args.password)


if __name__ == '__main__':
    main()
