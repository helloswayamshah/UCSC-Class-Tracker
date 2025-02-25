import requests
from bs4 import BeautifulSoup
import time
from twilio.rest import Client
from dotenv import load_dotenv
import os
from pathlib import Path
import database as db

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

LINK = "https://my.ucsc.edu/"
def whatsapp_init():
    account_sid = os.getenv('SID')
    auth_token = os.getenv('AUTH')
    client = Client(account_sid, auth_token)
    return client

def send_message(message, client, userId):
    resp = client.messages.create(from_='whatsapp:+14155238886', to=f'whatsapp:{db.getPhone(userId)}', body=message+"\n"+LINK)
    while resp.error_code is not None:
        print(resp.error_message)
        resp = client.messages.create(from_='whatsapp:+14155238886', to=f'whatsapp:{os.getenv('PHONE_NUMBER')}', body=message)

def createMessage(data):
    return f"Class: {data['subject']} {data['catalog_nbr']} - {data['class_section']} \nTitle: {data['title']} \nEnrolled: {data['enrl_total']} \nCapacity: {data['enrl_capacity']} \nWaitlist: {data['waitlist_total']} \n **{int(data['enrl_capacity']) - int(data['enrl_total'])} SPOTS LEFT** \n\n {LINK}"

def handlePing(userId, message):
    chanel = db.getMedium(userId)
    if chanel == "W":
        client = whatsapp_init()
        send_message(message, client, userId)
    elif chanel == "E":
        pass
    elif chanel == "S":
        pass

def get_data(class_id, term, subject):
    res = []
    LINK = f"https://my.ucsc.edu/PSIGW/RESTListeningConnector/PSFT_CSPRD/SCX_CLASS_LIST.v1/{term}?subject={subject}&catalog_nbr={class_id}"

    session = requests.Session()

    response = session.get(LINK)
    if response.status_code == 404:
        return res
    data = response.json()
  
    for i in data['classes']:
        res.append(i)
    return res

def getQuarter(quarter):
  formData = {"action": "results", 
                "binds[:term]": "invalid",
                "binds[:reg_status]": "all",
                "binds[:subject]": "",
                "binds[:catalog_nbr_op]": "=",
                "binds[:catalog_nbr]": "",
                "binds[:title]": "",
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
  response = requests.post('https://pisa.ucsc.edu/cs9/prd/sr9_2013/index.php', formData, headers={'Content-Type':'application/x-www-form-urlencoded'})
  soup = BeautifulSoup(response.content, 'html.parser')
  term = soup.find_all(id = "term_dropdown")
  quarters = term[0].find_all("option")
  res = {}
  for q in quarters:
    res[q.text] = q['value']
  # print(res)
  try:
    return res[quarter]
  except:
    return "invalid"

def trackClasses(userId, classes, quarterCode):
  trackerIds = db.getTrackerIds()
  print(trackerIds)
  if userId in trackerIds:
    db.updateTracker(userId, classes, quarterCode, {})
  else:
    db.trackClasses(userId, classes, quarterCode)
  return True

def stopTracking(userId):
  trackerIds = db.getTrackerIds()
  if userId not in trackerIds:
    return False
  db.stopTracking(userId)
  return True

def keepTracking():
  trackers = db.getTrackers()
  for tracker in trackers:
    userId = tracker[0]
    classes = tracker[1]
    quarterCode = tracker[2]
    cache = tracker[3]
    for c in classes:
      data = get_data(c["code"], quarterCode, c["subject"])
      for d in data:
        dclass = d['subject'] + ' ' + d['catalog_nbr']
        if dclass not in cache.keys():
          cache[dclass] = d
          if d['enrl_total'] < d['enrl_capacity']:
            message = createMessage(d)
            handlePing(userId, message)
          db.updateTracker(userId, classes, quarterCode, cache)
        elif cache[dclass] != d:
          message = createMessage(d)
          handlePing(userId, message)
          cache[dclass] = d
          db.updateTracker(userId, classes, quarterCode, cache)
    
def signup(data):
    try:
        db.handleSignup(data)
        return True
    except(Exception) as e:
        print(e)
        return False

def signin(data):
    try:
        result = db.handleSignin(data)
        if result:
            return True
        else:
            return False
    except(Exception) as e:
        print(e)
        return False

# client = whatsapp_init()

# classes = [102, 103, "114a", "115a", "180", "186"] #Change the classes here
# Subject = "CSE" #Change the subject here
# term = "2250" #Change the term here

# cached_status = {}
# cached_spots = {}
# init = True

