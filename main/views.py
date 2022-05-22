import json
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json


# Create your views here

def index(request):
    return render(request, 'index.html')

def login(request):
    cin = request.POST['cin']
    password = request.POST['password']
    status_code, response_data = get_inp(cin, password)
    if response_data != {'error': 'Not found'}:
        with open("/home/pi/Desktop/e-health-appareil/inp.json", "w") as inp_file:
            json.dump(response_data, inp_file)
        inp_file.close
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_inp(cin, password):

    DATA = {
        "username": cin,
        "password": password
    }
    r = requests.get("http://3.18.29.109/json_check/", params=DATA)
    return r.status_code, r.json()
