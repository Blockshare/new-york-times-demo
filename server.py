# Loading developer libraries

import requests
import os
import urllib
from flask import Flask, request
from flask import send_from_directory
from two1.wallet import Wallet
from two1.bitserv.flask import Payment
import json
import yaml

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

# go to http://developer.nytimes.com/ and choose the top-stories API key.
# This is my personal developer key
api_key = "5ea06aaaaf60d6dba5f9b06226bdfe0d:6:54078972"

# Adding 402 end-point
@app.route('/top-stories', methods=['GET', 'POST'])
@payment.required(5000)
def top_stories():
     """
     Choose the section of the NYTimes you would like to read
     """
     section = request.form['section']
     url = requests.get('http://api.nytimes.com/svc/topstories/v1/'+section+'.json?api-key='+api_key)
     return url.text

@app.route('/manifest')
def docs():
    """ Serves the app manifest to the 21 crawler """
    with open('manifest.yaml', 'r') as f:
        manifest_yaml = yaml.load(f)
    return json.dumps(manifest_yaml)

@app.route('/client')
def client():
     return send_from_directory('static', 'client.py')

if __name__=='__main__':
     app.run(host='0.0.0.0', port=5000)
