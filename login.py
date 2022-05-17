import json
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as rfid


def read_tag():
    reader = rfid()
    try:
        print("place tag")
        id, text = reader.read()
        return id
    finally:
        GPIO.cleanup()


def add_visit(medcin_id):
    patient_id = -999999
    while True:
        patient_id = print(read_tag())
        if(patient_id != -999999):
            DATA = {"patient": patient_id,
                    "medcin": medcin_id
                    }
            r = requests.post("http://3.18.29.109/doctor/create_visite", DATA)

            print(r.status_code)


if __name__ == '__main__':
    with open("./inp.json", "r") as inp_f:
        inp = json.load(inp_f)['INP']
    inp_f.close()
    print(inp)
    add_visit(inp)
