import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhackerrank.settings")
import django
django.setup()
from myservices.models import Problem
import re

for root, subdirs, files in os.walk('./problems'):
	for f in files:
		regexp = re.compile('\.\/problems\/(.*)')
		level = regexp.search(root).group(1)
		regexp2 = re.compile('(.*)\.')
		name = regexp2.search(f).group(1)
		p = Problem(difficulty=level, problem_name=name, problem_path=os.path.join(root, f))
		p.save()
	