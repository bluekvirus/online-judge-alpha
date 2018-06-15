from django.contrib import admin

# Register your models here.
from .models import Interview, Candidate, Submission, Problem

class InterviewAdmin(admin.ModelAdmin):
	readonly_fields = ('hash_str', 'created_at' , 'started_at')

class CandidateAdmin(admin.ModelAdmin):
	readonly_fields = ('created_at',)

admin.site.register(Interview, InterviewAdmin)
admin.site.register(Candidate, CandidateAdmin)
#admin.site.register(Submission)
admin.site.register(Problem)
