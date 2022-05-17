import json
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json


# Create your views here.

def hello(request):
    return render(request, 'index.html')


def login(request):
    cin = request.POST['cin']
    password = request.POST['password']
    status_code, response_data = get_inp(cin, password)
    print(response_data)
    if status_code == 200:
        with open("./inp.json", "w") as inp_file:
            json.dump(response_data, inp_file)
        inp_file.close
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_inp(cin, password):

    DATA = {
        "username": cin,
        "password": password
    }
    r = requests.post("http://3.18.29.109/json_check/", DATA)
    return r.status_code, r.json()
