from django.shortcuts import render
from .forms import EmailForm
# Create your views here.
def landing(request):
	form = EmailForm()
	return render(request,'myservices/landing.html', {'form': form})

