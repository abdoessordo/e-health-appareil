from time import sleep
import requests

cin = "K570940"
password = "Tanger.2001"

def add_visit(patient_id, medcin_id):

    DATA = {"patient": patient_id,
            "medcin": medcin_id
            }
    r = requests.post("http://3.18.29.109/doctor/create_visite", DATA)

    print(r.status_code)


def get_inp(cin, password):

    DATA = {
        "username": cin,
        "password": password
    }
    r = requests.post("http://3.18.29.109/json_check/", DATA)
    print(r.status_code)
    print(r.json())


if __name__ == '__main__':
    add_visit(5, 123456)
    # get_inp(cin, password)

