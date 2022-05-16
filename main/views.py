from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
import requests


# Create your views here.

def hello(request):
    return render(request, 'index.html')


def login(request):
    cin = request.POST['cin']
    password = request.POST['password']
    status_code, server_response = get_inp(cin, password)
    with open(".")
    return HttpResponse("Hello")


def get_inp(cin, password):

    DATA = {
        "username": cin,
        "password": password
    }
    r = requests.post("http://3.18.29.109/json_check/", DATA)
    return r.status_code, r.json()
