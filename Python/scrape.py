import requests
import json
import sys
from practice import tracks
tracks()
def search(t):
	if len(t) < 6:
		sys.exit()
	else:
		response = requests.get('https://itunes.apple.com/search?entity=song&limit=10&term=' + t)
		# print(json.dumps(response.json(), indent=2))
		data = response.json()
		hold =[]
		for info in data['results']:
			hold.append(info['trackName'])
			print(info['trackName'])
		return hold
def ok():
	print('Program finished')
def main():
	search(sys.argv[1])
	ok()
if __name__ == "__main__":
	main()