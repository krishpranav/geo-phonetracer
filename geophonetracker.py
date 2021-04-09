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