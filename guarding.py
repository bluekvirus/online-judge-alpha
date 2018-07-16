import subprocess
import time
import re
import sys
import json
import requests
import os

cmd = ['/usr/local/bin/phantomjs', '/hackerrank.js']
for i in range(40):
	try:
		p = subprocess.run(cmd, timeout=60, stdout=subprocess.PIPE)
	except subprocess.TimeoutExpired:
		print("Subprocess timed out")
		time.sleep(300) #sleep for 5 minutes before retry again
	else:
		ret  = p.stdout.decode().rstrip()
		if( ret == "Unable to access network" or not ret):
			print("Error")
			time.sleep(300)
			continue
		regexp = re.compile('hrank=(.*)')
		regexp2 = re.compile('auth-token=(.*)')
		res = regexp.search(ret).group(1)
		token = regexp2.search(ret).group(1)
		info = {'hrank' : res, 'csrf' : token}
		f = open('/app/hrank.txt', 'w')
		json.dump(info, f)
		f.close()
		message = sys.argv[1] + ': ' + res
		d = {'text': message}
		#use json not data= or will have invalid payload 400 bad request
		response = requests.post("https://hooks.slack.com/services/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", json=d, headers={'Content-Type': 'application/json'})
		break



