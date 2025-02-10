import requests
from bs4 import BeautifulSoup
import time
from twilio.rest import Client
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path('.') / '.env'
LINK = "https://my.ucsc.edu/"
def whatsapp_init():
    account_sid = os.getenv('SID')
    auth_token = os.getenv('AUTH')
    client = Client(account_sid, auth_token)
    return client

def send_message(message, client):
    resp = client.messages.create(from_='whatsapp:+14155238886', to=f'whatsapp:{os.getenv('PHONE_NUMBER')}', body=message+"\n"+LINK)
    while resp.error_code is not None:
        print(resp.error_message)
        resp = client.messages.create(from_='whatsapp:+14155238886', to=f'whatsapp:{os.getenv('PHONE_NUMBER')}', body=message+"\n"+LINK)


def get_data(class_ids, term, subject, cached, cached_spots, client, initial):
    for class_id in class_ids:
        formData = {"action": "results", 
                    "binds[:term]": term,
                    "binds[:reg_status]": "all",
                    "binds[:subject]": subject,
                    "binds[:catalog_nbr_op]": "=",
                    "binds[:catalog_nbr]": str(class_id),
                    "binds[:title]":"",
                    "binds[:instr_name_op]": "=",
                    "binds[:instructor]": "",
                    "binds[:ge]": "",
                    "binds[:crse_units_op]": "=",
                    "binds[:crse_units_from]": "",
                    "binds[:crse_units_to]": "",
                    "binds[:crse_units_exact]": "",
                    "binds[:days]": "",
                    "binds[:times]": "",
                    "binds[:acad_career]": "",
                    "binds[:asynch]": "A",
                    "binds[:hybrid]": "H", 
                    "binds[:synch]": "S",
                    "binds[:person]": "P"}

        response = requests.post('https://pisa.ucsc.edu/cs9/prd/sr9_2013/index.php', formData, headers= {'Content-Type': 'application/x-www-form-urlencoded'})
        # print(response.content)

        soup = BeautifulSoup(response.content, 'html.parser')
        class_names = soup.find_all("a", id = lambda x: x and x.startswith("class_id_"))
        all_status = soup.find_all("span", class_="sr-only")
        all_spaces_unclean = soup.find_all("div", class_="col-xs-6 col-sm-3")
        all_spaces = []
        for i in range(2, len(all_spaces_unclean), 3):
            all_spaces.append(all_spaces_unclean[i])
        for c, s, sp in zip(class_names, all_status, all_spaces):
            # print(c, s, sp)
            class_name = c.text
            status = s.text
            space_tokens = sp.text.split()
            spaces = int(space_tokens[2]) - int(space_tokens[0])
            filled = int(space_tokens[0])
            capacity = int(space_tokens[2])
            print(class_name, status, spaces, filled, capacity)

            if class_name not in cached:
                cached[class_name] = status
                cached_spots[class_name] = spaces
            elif (cached[class_name] == "Closed" and status == "Open") or (cached_spots[class_name] != spaces and spaces > 0):
                send_message(f"{class_name} is now open! There are {spaces}({filled}/{capacity}) spots available.", client)
                cached[class_name] = status
                cached_spots[class_name] = spaces
            elif cached[class_name] == "Open" and status == "Closed":
                send_message(f"{class_name} is now closed.", client)
                cached[class_name] = status
                cached_spots[class_name] = spaces
            if cached[class_name] == "Open" and initial:
                send_message(f"{class_name} still has {spaces}({filled}/{capacity}) spots available.", client)
        print()

load_dotenv(dotenv_path=env_path)
client = whatsapp_init()

classes = [102, 103, "114a", "115a", "180", "186"] #Change the classes here
Subject = "CSE" #Change the subject here
term = "2250" #Change the term here

cached_status = {}
cached_spots = {}
init = True
while True:
    print(time.ctime())
    get_data(classes, term, Subject, cached_status, cached_spots, client, init)
    init = False
    time.sleep(60*15)