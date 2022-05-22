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

def add_visit():
    patient_id = -999999
    while True:
        with open("/home/pi/Desktop/e-health-appareil/inp.json", "r") as inp_f:
            inp = json.load(inp_f)['INP']
        inp_f.close()
        patient_id = read_tag()
        if(patient_id != -999999):
            patient_id = get_patient_id(patient_id)
            print(patient_id)
            print('scanned')       
            DATA = {"patient": patient_id,
                    "medcin": inp
                    }
            r = requests.post("http://3.18.29.109/doctor/create_visite", DATA)

            print(r.status_code)
            sleep(2)


if __name__ == '__main__':
    add_visit()
