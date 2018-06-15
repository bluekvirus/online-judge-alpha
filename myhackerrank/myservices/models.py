from django.db import models
from django import forms
import random
import string
from django.utils import timezone

#one to many relationship with interviews table
class Candidate(models.Model):
	user_name = models.EmailField()
	created_at = models.DateTimeField()
	def save(self):
		if not self.id:
			self.created_at = timezone.now()
		super(Candidate, self).save()
	def __str__(self):
		return 'Candidate: {}'.format(self.user_name)

#many to many relationship between interviews and problems
class Problem(models.Model):
	difficulty = models.CharField(max_length=20)
	problem_name = models.CharField(max_length=20)
	problem_path = models.CharField(max_length=64)
	#changes the display on the admin site and when you print
	def __str__(self):
		return '{} : {} : {}'.format(self.difficulty, self.problem_name, self.id)

#pass it length 64 for a 512 bits hash string
def random_string(length):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))


#does this need a foreign key to candidate with the one-to-one field
class Interview(models.Model):
	started_at = models.DateTimeField(null=True, default=None)
	status = models.CharField(max_length=20)
	hash_str = models.CharField(max_length=64) #access the problems using .problem_set.all()
	#access the submission ids using .hackerrank_set.all()
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
	problems = models.ManyToManyField(Problem)
	created_at = models.DateTimeField()

	def save(self):
		if not self.id:
			self.hash_str = random_string(64)
			self.created_at = timezone.now()
		super(Interview, self).save()

#each submission has a foreign key to the candidate it belongs to as well as the interview?? Many submissions for one interview and one candidate

class Submission(models.Model):
	user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
	submit_id = models.IntegerField()
	result = models.CharField(max_length=20)
	problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE) 
	interview = models.ForeignKey(Interview, on_delete=models.CASCADE) 





