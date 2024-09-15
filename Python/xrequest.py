import sys
import requests
from requests_oauthlib import OAuth1
import csv
import json


post_url = 'https://api.twitter.com/2/tweets'
ul_param = {
  'user.fields': 'created_at,description,location,protected,public_metrics,url,verified'
}
Auth_param = {}

def fetch_auth_param():
  with open('keys.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
      Auth_param.update({row['name']: row['token']})
  

def authenticate():
  # OAuth function not applicable in user lookup function
  auth_data = OAuth1(Auth_param['Api_key'],Auth_param['Api_secret_key'],Auth_param['Access_token'],Auth_param['Access_token_secret'])
  return auth_data


def user_lookup(user_name):
  lookup_url = f'https://api.twitter.com/2/users/by/username/{user_name}'
  headers = {'Authorization': f"Bearer {Auth_param['bearer_token']}"}
  response = requests.get(lookup_url, headers=headers, params=ul_param)
  if response.status_code == 200:
	  return ul_response(response.json())
    
  else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")

def post_tweet(text):
  headers = {
    'Content-Type': 'application/json'
  }
  data = {
    'text': text
  }
  
  response = requests.post(post_url, json=data, auth=authenticate())
  
  if response.status_code == 201 or response.status_code ==200:
    return post_outsave(response.json())
  else:
    print(f"Failed to post tweet: {response.status_code} - {response.text}")
    return None

def fselector():
  if len(sys.argv[1:3]) == 2:
    if sys.argv[1] == 'ul' or sys.argv[1] == 'p':
      if sys.argv[1] == 'ul':
        user_lookup(sys.argv[2])
      else:
        post_tweet(sys.argv[2])
    elif sys.argv[1] == 'd':
      print(post_delete(sys.argv[2]))
    else:
      print(''' Enter *ul* to perform a user lookup
      
      Enter *p* to post a Tweet
      
      Enter *d* to delete followed by the tweet ID
      
      Examples:
      python xrequests.py ul "username"  # Do not include the '@' symbol
      python xrequests.py p "Tweet text"  # Enclose tweet text in quotes
      python xrequests.py ul "ID" 
      ''')
      
  else:
    print('''
    Usage: python filename.py <action> <content>
    
    <Action> options:
    ul  -  Perform a user lookup (do not include the '@' symbol in the username).
    p   -  Post a tweet with the specified text.
    
    d   - delete a tweet with specified ID
    Examples:
    python xrequests.py ul username
    python xrequests.py t "Your tweet text here"  # Enclose tweet text in quotes
    python xrequests.py d ID
    ''')
    
    sys.exit()



def ul_response(server_response):
  key_mapping = {
    'followers_count': 'Followers',
    'following_count': 'Following',
    'tweet_count': 'Tweets',
    'like_count': 'Likes'
  }
  response = server_response
  public_metrics = response['data']['public_metrics']
  Data = response['data']
  Date, Time = (Data['created_at']).split('T')
  Data.pop('created_at')
  Data.update({'Date': Date})
  Data.update({'Time': Time[:8]})
  updated_public_metrics = {key_mapping.get(key, key): value for key, value in public_metrics.items()}
  key_mapping_Data = {
    'id': 'UserID',
    'username': 'Username',
    'name': 'Full Name',
    'created_at': 'Account Created Time',
    'description': 'Bio',
    'location': 'Location',
    'verified': 'Verification Status'
  }
  updated_Data = {key_mapping_Data.get(key, key): value for key, value in Data.items() if key != 'public_metrics'}
  updated_Data['public_metrics'] = updated_public_metrics
  response['data'] = updated_Data
  ul_outsave(response)
  return response



def ul_outsave(response):
  # Check if 'data' exists and is a dictionary
  if 'data' in response and isinstance(response['data'], dict):
    print('successful!!')
    # Open the CSV file for appending and ensure no newline issues
    with open('ul_response.csv', 'w', newline='') as file:
      fieldnames = ['Fields', 'Data']
      writer = csv.DictWriter(file, fieldnames=fieldnames)

      # Write header if the file is empty
      file.seek(0)  # Move to the start of the file
      if file.tell() == 0:  # If the position is 0, there's no content yet
        writer.writeheader()

      # Process each key-value pair in the response
      for key, value in (response['data']).items():
        if key == 'public_metrics':
          for metric, count in value.items():
            writer.writerow({'Fields': metric, 'Data': count})
            print(f'{metric}: {count}')
        else:
          writer.writerow({'Fields': key, 'Data': value})
          print(f'{key}: {value}')
  else:
    print("Error: 'data' field is missing, empty, or not a dictionary in the response.")
    print(response.text)

def post_outsave(response):
  if 'data' in response:
    print('Tweet posted successfully')
    with open ('post_response.csv', 'w') as file:
      header = ['Fields', 'Data']
      writer = csv.DictWriter(file, fieldnames = header)
      writer.writeheader()
      for key, value in (response['data']).items():
        if key == 'edit_history_tweet_ids':
          for data in value:
            writer.writerow({'Fields': key, 'Data': data})
            print(f'{key}:{data}')
        else:
          writer.writerow({'Fields': key, 'Data': value})
          print(f'{key}:{value}')
  else:
    print(response.text)


def post_delete(id):
  d_url = f'https://api.twitter.com/2/tweets/{id}'
  response = requests.delete(d_url, auth = authenticate())
  if response.status_code == 201 or response.status_code == 200:
    if 'data' in response:
      for key,value in response['data']:
        result = f'Post deleted, server response\n{key,value}'
        print(result)
      return result
  else:
    print(f'Failed to delete tweet: {response.status_code} - {response.text}')
    return f'Failed to delete tweet: {response.status_code} - {response.text}'
    
  
  
def main():
  fetch_auth_param()
  fselector()
  
  
if __name__ == '__main__':
  main()