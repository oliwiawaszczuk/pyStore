from django.shortcuts import render
from django.template import loader


def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')