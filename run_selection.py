import timestamp
import json

def configured_environments():
	with open('environments.json') as file:
		return json.loads(file.read())