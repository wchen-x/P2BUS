from django.shortcuts import render
from django.http import HttpResponse

# admin login
# admin 
# Chen's usual password

def home(request):
    return render(request, "home.html", {})