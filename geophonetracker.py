#!/usr/bin/env/python

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m' # white

from shutil import which

print(G + '[+]' + C + ' Checking Dependencies...' + W)
pkgs = ['python3', 'pip3', 'php', 'ssh']
inst = True
for pkg in pkgs:
    present = which(pkg)
    if present == None:
        print(R + '[-] ' + W + pkg + C + ' is not Installed!')
        inst = False
    else:
        pass

if inst = False:
    exit()
else:
    pass

import os
import csv
import sys
import time
import json
import argparse
import requests
import subprocess as subp

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subdomain', help='Provide Subdomain for Serveo URL ( Optional )')
parser.add_argument('-k', '--kml', help='Provide KML Filename ( Optional )')
parser.add_argument('-t', '--tunnel', help='Specify Tunnel Mode [ Available : manual ]')
parser.add_argument('-p', '--port', type=int, default=8080, help='Port for Web Server [ Default : 8080 ]')

args = parser.parse_args()
subdom = args.subdomain
kml_fname = args.kml
tunnel_mode = args.tunnel
port = args.port

row = []
info = ''
result = ''
version = '1.2.5'

def banner():
	print (G +
	r''' GEO PHONE TRACKER''' + W)
	print('\n' + G + '[>]' + C + ' Created By : ' + W + 'krishpranav')
	print(G + '[>]' + C + ' Version    : ' + W + version + '\n')


def ver_check():
    print(G + '[+]' + C + ' Checking for Updates.....', end='')
    ver_url = 'https://raw.githubusercontent.com/krishpranav/geo-phonetracer/master/version.txt'
    try:
        ver_rqst = requests.get(ver_url)
        ver_sc = ver_rqst.status_code
        if ver_sec == 200:
            github_ver = ver_rqst.text
            github_ver = github_ver.strip()

            if version == github_ver:
                print(C + '[' + G + ' Up-To-Date ' + C +']' + '\n')
            else:
                print(C + '[' + G + ' Available : {} '.format(github_ver) + C + ']' + '\n')
        else:
            print(C + '[' + R + ' Status : {} '.format(ver_sc) + C + ']' + '\n')
    except Exception as e:
        print('\n' + R + '[-]' + C + ' Exception : ' + W + str(e))

