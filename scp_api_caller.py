import json
import requests
from constants import *

def read_token():
  headers = {'Authorization': basic_auth,
             'accept': 'application/json'}
  return json.loads(requests.get(auth_url, headers= headers).text)['access_token']

def http_post_with_json(url, json):
    headers = {'accept': 'application/json',
             'Content-Type': 'application/json',
             'Authorization': "Bearer %s" % read_token()}
    return requests.post(url, headers = headers, json = json)

def http_post(url, payload, files):
  headers = {'accept': 'application/json',
             'Authorization': "Bearer %s" % read_token()}
  response = requests.post(url, headers = headers, data = payload, files = files)
  return response.text

def call_od_api(url, method):
  headers = {'accept': 'application/json',
             'Authorization': "Bearer %s" % read_token()}
  if method.lower() == 'get':
    return requests.get(url, headers = headers).text
  elif method.lower() == 'delete':
    return requests.delete(url, headers = headers).text

def call_api(url, payload, files):
  headers = {'APIKey': apikey,
           'Accept': 'application/json'}
  if files is None:
    headers['Content-Type'] = 'application/json'
    response = requests.post(url, data = payload, headers = headers)
  elif(payload is None):
    response = requests.post(url, headers = headers, files = files)
  else:
    response = requests.post(url, headers = headers, data = payload, files = files)
  return response.text
