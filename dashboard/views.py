from django.shortcuts import render

from django.shortcuts import render

def dashboard_home(request):
    return render(request, 'dashboard/home.html')
# Create your views here.
