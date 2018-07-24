from django.apps import AppConfig
from threading import Thread
from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import requests
import os



class MyservicesConfig(AppConfig):
	name = 'myservices'
	def worker(self):
		from .models import Submission
		print("starting worker")
		consumer = KafkaConsumer('hrank_results', bootstrap_servers='kafka:9092', api_version=(1,4,3), security_protocol="SASL_PLAINTEXT", sasl_mechanism='PLAIN', sasl_plain_username='user', sasl_plain_password='bitnami', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
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

	def ready(self):
			if os.getenv('WITHIN_DOCKER') != None:
				if not os.path.isfile('/app/noready.txt'):
					f = open('/app/noready.txt', 'w+')
					t = Thread(target=self.worker)
					t.start()




