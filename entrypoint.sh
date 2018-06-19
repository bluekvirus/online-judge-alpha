#!/bin/bash
touch /var/log/cron.log && cron && tail -f /var/log/cron.log & python3 manage.py runserver 0.0.0.0:8000 & python3 -u hrank-consumer.py
