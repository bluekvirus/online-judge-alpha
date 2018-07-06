from myservices.models import Submission
from myrest.serializers import SubmissionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view()
def getResults(request, hashstr):
	if len(request.query_params) == 0:
		query = Submission.objects.filter(interview__hash_str = hashstr)
	else:
		pid = request.query_params['pid']
		query = Submission.objects.filter(interview__hash_str=hashstr).filter(problem__id=pid).order_by('-submit_at')
	serializer = SubmissionSerializer(query, many=True)
	return Response(serializer.data) #what happens if empty list

@api_view()
def getInterview(request, hashstr):
	context = {
		'hashstr' : hashstr,
	}
	template = loader.get_template('myservices/interview.html')
	Response(template.render(context))


