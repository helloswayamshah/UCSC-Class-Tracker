import psycopg2 as pg
import os
import dotenv
from pathlib import Path
import json

env_path = Path('.') / '.env'
dotenv.load_dotenv(dotenv_path=env_path)

db = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
port = os.getenv('DB_PORT')

print(db, host, user, password, port)

conn = pg.connect(
  database=db,
  user=user,
  password=password,
  host=host,
  port=port)
cursor = conn.cursor()


def handleSignup(data):
  q = "INSERT INTO Users (email, phoneNo, password, pingMedium) VALUES (%s, pgp_sym_encrypt(%s, %s), crypt(%s, gen_salt('bf')), %s);"

  cursor.execute(q, (
    data['email'],
    data['phoneNo'],
    os.getenv('DB_ENCRYPT_KEY'),
    data['password'],
    data['pingMedium']
    ))
  conn.commit()
  return True

def handleSignin(data):
  q = "SELECT * FROM Users WHERE email = %s AND password = crypt(%s, password);"
  cursor.execute(q, (data['email'], data['password']))
  result = cursor.fetchall()
  return result[0] if len(result)> 0 else None

def getUserByEmail(email):
  q = "SELECT * FROM Users WHERE email = %s;"
  cursor.execute(q, (email,))
  result = cursor.fetchall()
  return result[0] if len(result)> 0 else None
 
def getUserByPhone(phoneNo):
  q = "SELECT * FROM Users WHERE phoneNo = pgp_sym_encrypt(%s, %s);"
  cursor.execute(q, (phoneNo, os.getenv('DB_ENCRYPT_KEY')))
  result = cursor.fetchall()
  return result[0] if len(result)> 0 else None

def getMedium(userId):
  q = "SELECT pingMedium FROM Users WHERE guid = %s;"
  cursor.execute(q, (userId,))
  result = cursor.fetchall()
  return result[0][0]

def getPhone(userId):
  q = "SELECT pgp_sym_decrypt(phoneNo, %s) FROM Users WHERE guid = %s;"
  cursor.execute(q, (os.getenv('DB_ENCRYPT_KEY'), userId))
  result = cursor.fetchall()
  return result[0][0]

def getTrackerIds():
  q = "SELECT guid FROM Trackers;"
  cursor.execute(q)
  conn.commit()
  result = cursor.fetchall()
  return [i[0] for i in result]

def trackClasses(userId, classes, quarterCode):
  q = "INSERT INTO Trackers (guid, courses, term, cache) VALUES (%s, %s, %s, %s);"
  cursor.execute(q, (userId, json.dumps(classes), quarterCode, json.dumps({})))
  conn.commit()
  return True

def updateTracker(userId, classes, quarterCode, cache):
  q = "UPDATE Trackers SET courses = %s, term = %s, cache = %s WHERE guid = %s;"
  cursor.execute(q, (json.dumps(classes), quarterCode, json.dumps(cache), userId))
  conn.commit()
  return True

def stopTracking(userId):
  q = "DELETE FROM Trackers WHERE guid = %s;"
  cursor.execute(q, (userId,))
  conn.commit()
  return True

def getTrackers():
  q = "SELECT * FROM Trackers;"
  cursor.execute(q)
  result = cursor.fetchall()
  return result
