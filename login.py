import json
from sqlite3 import connect
import requests
import serial
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
    print(f"DATA_CARD = {DATA}")
    r = requests.post("http://3.18.29.109/card/", DATA)
    print(r.status_code)
    if r.status_code == 200 and r.status_code != {'error': 'Not found'}:
        return r.json()['pat']


def add_visit_med(medcin, patient):
    DATA = {"patient": patient,
            "medcin": medcin
            }
    print(f"DATA_med = {DATA}")

    r = requests.post("http://3.18.29.109/doctor/create_visite", DATA)

    print(r.status_code)


def add_visit_pharm(pharmacie, patient):
    DATA = {"patient": patient,
            "pharma": pharmacie
            }
    print(f"DATA_pharm = {DATA}")
    
    r = requests.get("http://3.18.29.109/pharmacie/create_visite", DATA)

    print(r.status_code)


def send_request():
    
    while True:
        connected = False
        while not connected:
            try:
                ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
                connected = True
            except:
                connected = False

        if connected:
            patient_id = ser.readline().decode().strip('\n').strip('\r')
            if patient_id:
                with open("/home/pi/Desktop/e-health-appareil/inp.json", "r") as inp_f:
                    response = json.load(inp_f)
                    inp = response['INP']
                    role = response['role']
                inp_f.close()
                try:
                    patient_id = get_patient_id(patient_id)
                    user_found = True
                except:
                    user_found = False
                    print("user not found")
    
                if user_found:
                    if role == 'pharmacie':
                        add_visit_pharm(inp, patient_id)
                    elif role == 'doctor':
                        add_visit_med(inp, patient_id)
                sleep(2)
        ser.close()

if __name__ == '__main__':
    send_request()
