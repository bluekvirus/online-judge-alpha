from express.decorators import service, methods, url
import os
from django.conf import settings 
import requests
import json
from myservices.models import Submission, Problem, Interview, Candidate
from kafka import KafkaProducer
from django.core import serializers
from django.utils import timezone
from django.template import loader
from django.db.models import Q
from .forms import EmailForm


@url('interview/getAuth')
@service
def getAuth(req, res, *args, **kwargs):
	f = open('/app/hrank.txt', "r")
	contents = json.load(f)
	res.json(contents)

@url('interview/([a-zA-Z0-9]*)/submit')
@methods('POST')
@service
def postSubmission(req, res, hashstr, *args, **kwargs):
	code = req.json['code']
	language = req.json['language']
	pid = req.json['pid'] #does this become problem id then??
	j = {'code': code, 'language':language, 'contest_slug': 'master'}
	query = Interview.objects.filter(hash_str=hashstr).filter(status="Started")
	if query:
		#check how much time has elapsed. for now leave it at 3 hours for max
		currtime = timezone.now()
		if((timezone.now() - query[0].started_at).total_seconds() > 3600): #10800
			query[0].status = "Completed" #should this be here?
			query[0].save()
			return res.json({"Timeup": "Interview has ended" })
		#blockSubmit = Submission.objects.filter(interview__hash_str = hashstr).filter(problem__id=pid).filter(result)
		blockSubmit = Submission.objects.filter(Q(interview__hash_str = hashstr), Q(problem__id = pid), Q(result="Processing") |
			Q(result="Queued") | Q(result = None))
		if query[0].problems.filter(id=pid).exists() and not blockSubmit:
			f = open('/app/hrank.txt', "r")
			contents = json.load(f)
			f.close()
			problem = Problem.objects.get(id=pid)
			interview = query[0]
			b = Submission(interview=interview, submit_id=None, result=None, problem=problem)
			b.save()
			response = requests.post('https://www.hackerrank.com/rest/contests/master/challenges/' + problem.problem_name + '/submissions', json=j, headers={'Content-Type': 'application/json', 'X-CSRF-Token': contents['csrf']}, cookies={'_hrank_session': contents['hrank']})
			ret = response.json()
			status = ret['model']['status']
			submit_id = ret['model']['id']
			if(status == "Processing" or status == "Queued"):
				producer = KafkaProducer(bootstrap_servers='kafka:9092', api_version=(1,4,3), security_protocol="SASL_PLAINTEXT", sasl_mechanism='PLAIN', sasl_plain_username='user', sasl_plain_password='bitnami', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
				producer.send('hrank_results', {'sid': submit_id, 'problem': problem.problem_name})
			b.submit_id = submit_id
			b.result = status
			b.save()
			return res.json({'submit_id': submit_id, 'result': status, 'submit_at': b.submit_at})
	return res.json({"Error": "Cannot Submit"})

@url('interview/([a-zA-Z0-9]*)/results')
@methods('GET')
@service #should it still be uid or do i get this from the hashstr portion and then find uid
def getResults(req, res, hashstr, *args, **kwargs):
	if(len(req.params) == 0):
		query = Submission.objects.filter(interview__hash_str = hashstr)
		qjson = serializers.serialize('json', query)
		j = json.loads(qjson)
		return res.json(j, safe=False)
	elif(len(req.params) == 1): #used to get all submission history initially in the front end side
		pid = req.params['pid'] #this is the problem id
		query = Submission.objects.filter(interview__hash_str=hashstr).filter(problem__id=pid).order_by('-submit_at') #have to add some additional query because now the submission table should have problem id not name
		qjson = serializers.serialize('json', query)
		j = json.loads(qjson)
		return res.json(j, safe=False)
	return res.json([], safe=False)


@url('interview/([a-zA-Z0-9]*)/poll')
@methods('GET')
@service
def pollResult(req, res, hashstr, *args, **kwargs):
	#called by front end to poll for in process result
	pid = req.params['pid']
	sid = req.params['sid']
	query = Submission.objects.filter(interview__hash_str=hashstr).filter(problem__id = pid).filter(submit_id=sid) #weird line
	qjson = serializers.serialize('json', query)
	j = json.loads(qjson)
	if not j:
		return res.json({"Error", "Invalid interview, submission id, or problem id"})
	return res.json(j, safe=False)

@url('interview/([a-zA-Z0-9]*)/problems')
@methods('GET')
@service
def getProblems(req, res, hashstr, *args, **kwargs):
	#this one will check validity of the hash string passed in as 
	query = Interview.objects.filter(hash_str=hashstr)
	if not query: #or query.exist()
		#return res.json({"Error": "404 interview does not exist"}) 
		template = loader.get_template('myservices/404.html')
		res.html(template.render())
		res.status(404)
	else:
		#is valid so we should return a page with start button or problems if already started
		started = query[0].started_at
		if not started:
			#we need to return the start button
			#return res.json({"Valid":"Valid interview that has not been started"})
			template = loader.get_template('myservices/welcomepage.html')
			context = {
				'hashstr' : hashstr,
			}
			res.html(template.render(context))
			res.status(200)
		else:
			problem_list = query[0].problems.all()
			context = {
				'hashstr' : hashstr,
				'interview_problems' : problem_list,
			}
			template = loader.get_template('myservices/problem.html')
			res.html(template.render(context))

 
@url('interview/([a-zA-Z0-9]*)/start')
@methods('GET')
@service
def startInterview(req, res, hashstr, *args, **kwargs):
	query = Interview.objects.get(hash_str=hashstr)
	if(query.started_at != None):
		return res.json({"Already Started": "Interview was already started"}) #what to return in this case??
	query.started_at = timezone.now()
	query.status = "Started"
	query.save()
	return res.json({"Successful Start": "Interview is now started"})

@url('interview/([a-zA-Z0-9]*)/time')
@methods('GET')
@service
def getTime(req, res, hashstr, *args, **kwargs):
	query = Interview.objects.filter(hash_str=hashstr)
	if(query):
		return res.json({"Time":query[0].started_at})
	return res.json({"Time": 0})

@url('interview/hello')
@methods('GET')
@service
def welcome(req, res, *args, **kwargs):
	return res.html( '<div style = "text-align: center; font-size: 40px;">' + '<p style="color: 5F9EA0"> Hello World! </p>' + '</div>')

@url('interview/([a-zA-Z0-9]*)')
@methods('GET')
@service
def getInterview(req, res, hashstr, *args, **kwargs):
	context = {
		'hashstr' : hashstr,
	}
	template = loader.get_template('myservices/interview.html')
	res.html(template.render(context))
	res.status(200)

@url('interview')
@methods('POST')
@service
def formPost(req, res, *args, **kwargs):
	form = EmailForm(req.POST)
	context = {}
	if form.is_valid():
		email = form.cleaned_data['user_email']
		query = Interview.objects.filter(candidate__user_name = email).exclude(status="Completed").order_by('created_at')
		if query:
			print("query is",query[0])
			context['hashstr'] =  query[0].hash_str
		template = loader.get_template('myservices/interview.html')
		res.html(template.render(context))
		res.status(200)
