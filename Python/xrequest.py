import sys
import requests
import csv
import json
def get_key():
	with open('keys.csv', 'r') as file:
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
