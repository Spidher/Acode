import sys
import requests
from requests_oauthlib import OAuth1
import csv
import json
import pytz
from datetime import datetime

post_url = 'https://api.twitter.com/2/tweets'
param = {
  'user.fields': 'created_at,description,location,protected,public_metrics,url,verified'
}
Auth_param = {}

def fetch_auth_param():
  with open('keys.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
      Auth_param.update({row['name']: row['token']})
  Auth_param.update({'timestamp': gen_time()})

def authenticate():
  # OAuth function not applicable in user lookup function
  auth_data = OAuth1(Auth_param['Api_key'],Auth_param['Api_secret_key'],Auth_param['Access_token'],Auth_param['Access_token_secret'],Auth_param['timestamp'])
  return auth_data

def gen_time():
  # Get the current time in UTC
  utc_now = datetime.now(pytz.UTC)
  # Convert the datetime to Unix timestamp
  timestamp = int(utc_now.timestamp())
  return str(timestamp)

def user_lookup(user_name=sys.argv[2]):
  lookup_url = f'https://api.twitter.com/2/users/by/username/{user_name}'
  headers = {'Authorization': f"Bearer {Auth_param['bearer_token']}"}
  response = requests.get(lookup_url, headers=headers, params=param)
  if response.status_code == 200:
    print("X Query sent, response pkg unpacked")
    return json.dumps(response.json(), indent=2)
  else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")

def post_tweet(text=sys.argv[2]):
  headers = {
    'Authorization': f"Bearer {Auth_param['bearer_token']}",
    'Content-Type': 'application/json'
  }
  data = {
    'text': text
  }

  response = requests.post(post_url, json=data, auth = authenticate())

  if response.status_code == 201:
    print("Tweet posted successfully!")
    return response.json()
  else:
    print(f"Failed to post tweet: {response.status_code} - {response.text}")
    return None

def fselector():
  if sys.argv[1:3]:
    if sys.argv[1] == 'ul' or sys.argv[1] == 't':
      if sys.argv[1] == 'ul':
        user_lookup()
      else:
        post_tweet()
    else:
      print(''' enter *ul* to run x user look up

      *t* to post a tweet

      e.g python xrequests.py ul <username> N:B do not add the *@* symbol

      e.g2 python xrequest.py t *Tweet text*
      -- text must be put in quotations (" ") ''')
      sys.exit()
  else:
    print('''
    specify task after file name

    supported syntax -- python filename.py <action> <content>

    enter *ul* to run x user look up

    *t* to post a tweet

    e.g python xrequests.py ul <username> N:B do not add the *@* symbol

    e.g2 python xrequest.py t *Tweet text*
    -- text must be put in quotations (" ")

    ''')
    sys.exit()

def main():
  fetch_auth_param()
  fselector()

if __name__ == '__main__':
  main()