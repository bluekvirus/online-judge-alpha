from express.decorators import service, methods, url
import os
from django.conf import settings 
import requests
import json
from myservices.models import Submission, Problem, Interview, Candidate
from kafka import KafkaProducer
from django.core import serializers
from django.utils import timezone


@service
def getAuth(req, res, *args, **kwargs):
	f = open('/app/hrank.txt', "r")
	contents = json.load(f)
	res.json(contents)

@url('interview/([a-zA-Z0-9]*)/submit')
@methods('POST')
@service
def postSubmission(req, res, hashstr, *args, **kwargs):
	f = open('/home/cherie/Desktop/docker-hrank/myhackerrank/myservices/hrank.txt', "r")
	contents = json.load(f)
	f.close()
	code = req.json['code']
	language = req.json['language']
	pid = req.json['problem-id'] #does this become problem id then??
	iid = req.json['interview_id']
	j = {'code': code, 'language':language, 'contest_slug': 'master'}
	query = Interview.objects.filter(hash_str=hashstr)
	if not query:
		return res.json({'Error': 'Interview not found'})
	#first make sure the problem id is actually one of the candidates problems
	if query[0].problems.filter(id=pid).exists():
		problem = Problem.objects.get(id=pid)
		interview = Interview.objects.get(id=iid)
		response = requests.post('https://www.hackerrank.com/rest/contests/master/challenges/' + problem.problem_name + '/submissions', json=j, headers={'Content-Type': 'application/json', 'X-CSRF-Token': contents['csrf']}, cookies={'_hrank_session': contents['hrank']})
		j = response.json()
		status = j['model']['status']
		submit_id = j['model']['id']
		if(status == "Processing" or status == "Queued"):
		#	producer = KafkaProducer(bootstrap_servers='kafka:9092', security_protocol="SASL_PLAINTEXT", sasl_mechanism='PLAIN', sasl_plain_username='user', sasl_plain_password='bitnami', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
		#	producer.send('hrank_results', {'sid': submit_id, 'problem': problem.problem_name})
			b = Submission(interview=interview, submit_id=submit_id, result=status, problem=problem)
			b.save()
			return res.json({'submit_id': submit_id, 'submission_status': 'Submitted successfully, currently processing'})
		b = Submission(interview = interview, submit_id=submit_id, result=status, problem=problem)
		b.save()
		return res.json({'submit_id': submit_id, 'submission_status': status})
	return res.json({"Error": "Invalid Problem"})

@methods('GET')
@service #should it still be uid or do i get this from the hashstr portion and then find uid
def getResults(req, res, *args, **kwargs):
	if(len(req.params) == 1):
		iid = req.params['interview_id']
		query = Submission.objects.filter(interview__id = iid) 
		qjson = serializers.serialize('json', query)
		j = json.loads(qjson)
		return res.json(j, safe=False)
	elif(len(req.params) == 2):
		iid = req.params['interview_id']
		pid = req.params['pid'] #this is the problem id
		query = Submission.objects.filter(interview__id=iid).filter(problem__id=pid) #have to add some additional query because now the submission table should have problem id not name
		qjson = serializers.serialize('json', query)
		j = json.loads(qjson)
		return res.json(j, safe=False)
	return res.json([], safe=False)

@url('interview/([a-zA-Z0-9]*)/problems')
@methods('GET')
@service
def interview(req, res, hashstr, *args, **kwargs):
	#this one will check validity of the hash string passed in as 
	query = Interview.objects.filter(hash_str=hashstr)
	if not query: #or query.exist()
		return res.json({"Error": "404 interview does not exist"})
	else:
		#is valid so we should return a page with start button or problems if already started
		started = query[0].started_at
		if not started:
			#we need to return the start button
			return res.json({"Valid":"Valid interview that has not been started"})
		else:
			problem_list = query[0].problems.all()
			print(problem_list) #will give a query set back
			#the index returned matters because those problems should always be in that tab format
			#affects the submit button because embedded with the problem id??
			#return the problems via json array
			#need to stream/serialize the html
			ret = []
			ids = []
			for p in problem_list:
				ids.append(p.id)
				f = open(p.problem_path, 'r')
				ret.append(f.read().strip())
				f.close()
			return res.json({"Problems": ret, "Problem_Ids": ids}, safe=False)

 
@url('interview/([a-zA-Z0-9]*)/start')
@methods('GET')
@service
def startInterview(req, res, hashstr, *args, **kwargs):
	query = Interview.objects.get(hash_str=hashstr)
	if(query.started_at != None):
		return res.json({"Already Started": "Interview was already started"})
	query.started_at = timezone.now()
	query.save()
	return res.json({"Successful Start": "Interview is now started"})






