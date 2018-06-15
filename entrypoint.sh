#!/bin/bash
touch /var/log/cron.log && cron && tail -f /var/log/cron.log & python3 manage.py migrate --fake myservices zero && python3 manage.py makemigrations myservices && python3 manage.py migrate & python3 manage.py runserver 0.0.0.0:8000 & python3 -u hrank-consumer.py
