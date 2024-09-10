import pytest
import sys
import requests
from scrape import search

def test_search():
	hold = []
	with open('response.txt') as file:
		for line in file:
			hold.append(line.rstrip())
	# Test if the search function returns the first track name
	assert search('weezer') == hold