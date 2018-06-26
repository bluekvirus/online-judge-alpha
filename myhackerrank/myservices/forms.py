from django import forms

class EmailForm(forms.Form):
	user_email = forms.EmailField(label = 'Candidate Email')
