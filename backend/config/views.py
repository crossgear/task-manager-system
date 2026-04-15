from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def projects(request):
    return render(request, 'project.html')

def register(request):
    return render(request, 'register.html')