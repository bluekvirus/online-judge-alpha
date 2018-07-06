from rest_framework.serializers import ModelSerializer
from myservices.models import Submission


class SubmissionSerializer(ModelSerializer):
	class Meta:
		model = Submission
		fields = ('submit_id', 'result', 'submit_at')
