FROM python:3
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get install -y cron
RUN apt-get install -y libfreetype6 libfontconfig
RUN apt-get install -y wget
RUN wget -q https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN tar xjf phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN install -t /usr/local/bin phantomjs-2.1.1-linux-x86_64/bin/phantomjs
RUN rm -rf phantomjs-2.1.1-linux-x86_64
RUN rm phantomjs-2.1.1-linux-x86_64.tar.bz2
ADD crontab /etc/cron.d/extract
RUN chmod 0644 /etc/cron.d/extract
RUN crontab /etc/cron.d/extract
ADD hackerrank.js /hackerrank.js
ADD guarding.py /guarding.py
ADD entrypoint.sh .
ADD myhackerrank .
ADD wait-on-kafka.sh .
RUN chmod +x /entrypoint.sh
RUN chmod +x /guarding.py 
RUN chmod +x /wait-on-kafka.sh
VOLUME /var/log
VOLUME /app
ENTRYPOINT ["/wait-on-kafka.sh"]
