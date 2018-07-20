#!/bin/bash
printenv | sed 's/^\(.*\)$/export \1/g' > /app/project_env.sh && touch /var/log/cron.log && cron && tail -f /var/log/cron.log & python3 /app/myhackerrank/manage.py runserver 0.0.0.0:8000 
