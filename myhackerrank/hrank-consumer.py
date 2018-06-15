from kafka import KafkaConsumer
from kafka import KafkaProducer
import os
import json
import requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhackerrank.settings")
import django
django.setup()
from myservices.models import Submission


consumer = KafkaConsumer('hrank_results', bootstrap_servers='kafka:9092', api_version=(1,4,2), security_protocol="SASL_PLAINTEXT", sasl_mechanism='PLAIN', sasl_plain_username='user', sasl_plain_password='bitnami', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
f = open('/app/hrank.txt', "r")
contents = json.load(f)
while True:
	for msg in consumer:
		print(msg.value)
		m = msg.value
		problem = m['problem']
		sid = m['sid']
		response = requests.get('https://www.hackerrank.com/rest/contests/master/challenges/' + problem + '/submissions/' + str(sid), cookies={'_hrank_session': contents['hrank'] })
		ret = response.json()
		status = ret['model']['status']
		if(status == "Processing" or status == "Queued"):
			producer = KafkaProducer( bootstrap_servers='kafka:9092',security_protocol="SASL_PLAINTEXT", sasl_mechanism='PLAIN', sasl_plain_username='user', sasl_plain_password='bitnami', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
			producer.send('hrank_results', {'sid': sid, 'problem': problem})
		else:
			query= Submission.objects.get(submit_id=sid)
			query.result = status
			query.save()
