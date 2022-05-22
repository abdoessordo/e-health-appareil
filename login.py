import json
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as rfid
from time import sleep 

GPIO.setwarnings(False)


def read_tag():
    reader = rfid()
    try:
        print("place tag")
        id, text = reader.read()
        return id
    finally:
        GPIO.cleanup()

def get_patient_id(card_id):
    DATA = {"card": card_id}
    r = requests.post("http://3.18.29.109/card/", DATA)
    print(r.status_code)
    if r.status_code == 200 and r.status_code != {'error': 'Not found'}:
        return r.json()['pat']


def add_visit_med(medcin, patient):
    DATA = {"patient": patient,
            "medcin": medcin
            }
    r = requests.post("http://3.18.29.109/doctor/create_visite", DATA)

    print(r.status_code)


def add_visit_pharm(pharmacie, patient):
    DATA = {"patient": patient,
            "pharma": pharmacie
            }
    r = requests.get("http://3.18.29.109/pharmacie/create_visite", DATA)

    print(r.status_code)


def send_request():
    patient_id = -999999
    while True:
        with open("/home/pi/Desktop/e-health-appareil/inp.json", "r") as inp_f:
            inp = json.load(inp_f)['INP']
            role = json.load(inp_f)['role']
        inp_f.close()
        patient_id = read_tag()
        if(patient_id != -999999):
            patient_id = get_patient_id(patient_id)
            if role == 'pharmacie':
                add_visit_pharm(inp, role)
            elif role == 'doctor':
                add_visit_med(inp, role)
            sleep(2)


if __name__ == '__main__':
    send_request()
