import sys
import requests
<<<<<<< HEAD
import csv
import json
def get_key():
	with open('X_keys.csv', 'r') as file:
		reader = csv.DictReader(file)
		for row in reader:
			if row['name'] =='bearer_token' :
				return row['token']
 			
Header = {'Authorization': f'Bearer {get_key()}'}
search_query, max_results = sys.argv[1], int(sys.argv[2])
url = 'https://api.twitter.com/2/tweets/search/recent'
param ={
	'query': search_query,
 	'max_results': max_results,
 	'expansion' : 'reply_to_user_id',
 	'tweet.fields' : 'attachments',
 	'user.fields' : 'username',
 	'tweet.fields' : 'created_at,text'
}
def resp():
	response = requests.get(url,headers = Header,params = param)
	if response.status_code == 200:
		return f'Succesful {json.dump(response.json, indent =2)}'
	else:
		return 'Error sending request'

def main():
  print(resp())



if __name__ == '__main__':
  main()
=======
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

def user_lookup(user_name):
  lookup_url = f'https://api.twitter.com/2/users/by/username/{user_name}'
  headers = {'Authorization': f"Bearer {Auth_param['bearer_token']}"}
  response = requests.get(lookup_url, headers=headers, params=param)
  if response.status_code == 200:
    print("X Query sent, response pkg unpacked")
    return json.dumps(response.json(), indent=2)
  else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")

def post_tweet(text):
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
  if len(sys.argv[1:3]) == 2	:
    if sys.argv[1] == 'ul' or sys.argv[1] == 't':
      if sys.argv[1] == 'ul':
        user_lookup(sys.argv[2])
      else:
        post_tweet(sys.argv[2])
    else:
      print(''' Enter *ul* to perform a user lookup
      
      Enter *t* to post a tweet
      
      Examples:
      python xrequests.py ul "username"  # Do not include the '@' symbol
      python xrequests.py t "Tweet text"  # Enclose tweet text in quotes''')
  else:
    print('''
    Usage: python filename.py <action> <content>
    
    <Action> options:
    ul  -  Perform a user lookup (do not include the '@' symbol in the username).
    t   -  Post a tweet with the specified text.
    
    Examples:
    python xrequests.py ul username
    python xrequests.py t "Your tweet text here"  # Enclose tweet text in quotes
    ''')
    
    sys.exit()

def main():
  fetch_auth_param()
  fselector()

if __name__ == '__main__':
  main()
>>>>>>> xrequest
