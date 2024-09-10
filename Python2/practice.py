import sys
import json
import requests
	# Call the API directly t
def tracks(v = 'weezer', l= 10):
	response = requests.get(f'https://itunes.apple.com/search?entity=song&limit={l}&term={v}')
	data = response.json()
	if __name__ == '__main__':
		with open('response.txt', 'a') as resfile:
			resfile.write(f'Track by {v} \n')
	for info in data['results']:
		temp = info['trackName']
		with open('response.txt', 'a') as resfile:
			resfile.write(f'{temp}\n')
	print('Succesful')

def main():
	tracks(sys.argv[1], sys.argv[2])
	

if __name__ == '__main__':
	main()
