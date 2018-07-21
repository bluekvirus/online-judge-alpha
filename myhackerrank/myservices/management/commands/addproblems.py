from django.core.management.base import BaseCommand, CommandError
from myservices.models import Problem
import os
import re

class Command(BaseCommand):
    help = 'Adds the problems in problems folder into the DB'
    args = 'TAKES NO ARGUMENT'

    def handle(self, *args, **options):
        for root, subdirs, files in os.walk('../problems'):
            for f in files:
                regexp = re.compile('\.\/problems\/(.*)')
                level = regexp.search(root).group(1)
                regexp2 = re.compile('(.*)\.')
                name = regexp2.search(f).group(1)
                print(name)
                p = Problem(difficulty=level, problem_name=name, problem_path=os.path.join(root[2:], f))
                p.save()
        return
            