from flask import request, jsonify, Response
import requests
from flask_cors import CORS
import json
import controller
from connexion import FlaskApp
from connexion.options import SwaggerUIOptions
import time
import threading

def keepTracking():
  while True:
    print(time.ctime())
    controller.keepTracking()
    # time.sleep(60*15)
    time.sleep(10)

def activate_job():
  thread = threading.Thread(target=keepTracking, daemon=True)
  thread.start()

activate_job()

options = SwaggerUIOptions(swagger_ui_path="/docs")

app = FlaskApp(__name__, swagger_ui_options=options, strict_validation=True, validate_responses=True)
CORS(app.app)
app.add_api('./api/openapi.yaml', swagger_ui_options=options, validate_responses=True, strict_validation=True)

cache = {}
client = controller.whatsapp_init()

@app.route('/api/v1/classData', methods=['GET'])
def get_data():
  course = request.args.get('class')
  quarter = request.args.get('quarter')
  subject = request.args.get('subject')
  print(course, quarter, subject)
  q = controller.getQuarter(quarter)
  if q == "invalid":
    return Response(status=404, response=json.dumps({"message": "Wrong format or Quarter Not published"}), content_type='application/json')

  res = controller.get_data(course, q, subject)
  if len(res) == 0:
    return Response(status=404, response=json.dumps({"message": "No classes found"}), content_type='application/json')
  return jsonify(res)

@app.route('/api/v1/quarterCode', methods=['GET'])
def get_quarter():
  quarter = controller.getQuarter(request.args.get('quarter'))
  if quarter == "invalid":
    return Response(status=404, response=json.dumps({"message": "Wrong format or Quarter Not published"}), content_type='application/json')
  return jsonify(quarter)

@app.route('/api/v1/trackClasses/<userId>', methods=['POST'])
def track_classes(userId):
  track = request.args.get('track')
  if track == "true":
    classes = request.get_json()
    quarter = request.args.get('quarter')
    quarterCode = controller.getQuarter(quarter)
    if quarterCode == "invalid":
      return Response(status=404, response=json.dumps({"message": "Wrong format or Quarter Not published"}), content_type='application/json')
    controller.trackClasses(userId, classes, quarterCode)
    return Response(status=201, response=json.dumps({"message": "Classes are being tracked"}), content_type='application/json')
  else:
    if (controller.stopTracking(userId)):
      return Response(status=204, response=json.dumps({"message": "Classes are no longer being tracked"}), content_type='application/json')
    else:
      return Response(status=404, response=json.dumps({"message": "User not tracking"}), content_type='application/json')

@app.route('/api/v1/signup', methods=['POST'])
def signup():
  data = request.get_json()
  print(data)
  res = controller.signup(data)
  if res:
    return Response(status=201, response=json.dumps({"message": "User created"}), content_type='application/json')
  else:
    return Response(status=400, response=json.dumps({"message": "User already exists"}), content_type='application/json')

@app.route('/api/v1/signin', methods=['POST'])
def signin():
  data = request.get_json()
  res = controller.signin(data)
  if res:
    return Response(status=200, response=json.dumps({"message": "User signed in"}), content_type='application/json')
  else:
    return Response(status=400, response=json.dumps({"message": "Invalid User Id or Password"}), content_type='application/json')

if __name__ == '__main__':
  app.run(port=3010)
