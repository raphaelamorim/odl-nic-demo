#!/usr/bin/python
__author__ = "Cris Shumate"

import uuid
import json
import requests
import pprint
import sys

pp = pprint.PrettyPrinter(indent=2)

baseurl = "http://localhost:8181/restconf/config/"
mapurl = "intent-mapping-interface:mappings/"
outerurl = "outer-map/"
intentsurl = "intent:intents/"
intenturl = "intent/"


headers = {}
headers['Content-Type'] = 'application/json'

userId = 'admin'
password = 'admin'

mac1 = "15-73-8B-92-92-DA"
mac2 = "0B-D7-48-C0-9B-58"

def create_mapping(uid, name, value):
	url = baseurl + mapurl + outerurl + uid

	payload =	{
					"outer-map": [
						{
							"id": uid,
							"inner-map": [
								{
									"inner-key":name,
									"value":value
								}
							]
						}
					]
				}

	r = requests.put(url, headers=headers, auth=(userId, password), data=json.dumps(payload))

	print

	if r.status_code == 200:
		print 'created mapping of ' + name + ' to ' + value + ' successfully ' + '(' + uid + ')'
	else:
		print 'error creating mapping of ' + name + ' to ' + value

	print

def print_mappings():
	url = baseurl + mapurl

	r = requests.get(url, headers=headers, auth=(userId, password))

	if r.status_code != 200:
		print '\nerror retrieving mappings\n'
		return

	print '\nMappings:'
	print '------'

	mappings = json.loads(r.text)
	print

	for mapping in mappings['mappings']['outer-map']:
		print 'inner-map (id: ' + str(mapping['id']) + '):'
		print '\tinner-key:\t' + str(mapping['inner-map'][0]['inner-key'])
		print '\tvalue:\t\t' + str(mapping['inner-map'][0]['value'])
		print

	print '------\n'

def delete_mappings():
	url = baseurl + mapurl

	r = requests.delete(url, headers=headers, auth=(userId, password))

	print

	if r.status_code == 200:
		print ('mappings deleted')
	else:
		print ('error deleting mappings')

	print

def create_intent(uid, from_epg, to_epg, action):
	url = baseurl + intentsurl + intenturl + uid

	payload =	{
					"intent": [
						{
							"id": uid,
							"subjects": [
								{
									"order": "1",
									"end-point-group": {
										"name": to_epg
									}
								},
								{
									"order": "2",
									"end-point-group": {
										"name": from_epg
									}
								}
							],
							"actions": [
								{
									"order": "1",
									action: {}
								}
							]
						}
					]
				}

	r = requests.put(url, headers=headers, auth=(userId, password), data=json.dumps(payload))

	print

	if r.status_code == 200:
		print 'created intent (' + uid + ') successfully'
	else:
		print 'error creating intent'

	print

def print_intents():
	url = baseurl + intentsurl

	r = requests.get(url, headers=headers, auth=(userId, password))

	if r.status_code != 200:
		print 'error retrieving intents'
		return

	print '\nIntents:'
	print '------\n'

	intents = json.loads(r.text)
	
	for intent in intents["intents"]["intent"]:
		print 'Intent ' + intent["id"] + ":"
		print '\tFrom:   ' + intent["subjects"][0]["end-point-group"]["name"]
		print '\tTo:     ' + intent["subjects"][1]["end-point-group"]["name"]
		sys.stdout.write('\tAction: ')

		if "allow" in intent["actions"][0]:
			print 'allow\n'
		elif "block" in intent["actions"][0]:
			print 'block\n'
		elif "log" in intent["actions"][0]:
			print 'log\n'

	print '------\n'

def delete_intents():
	url = baseurl + intentsurl

	r = requests.delete(url, headers=headers, auth=(userId, password))

	print

	if r.status_code == 200:
		print ('intents deleted')
	else:
		print ('error deleting intents')

	print

def demo():
	create_mapping(str(uuid.uuid4()), "Mktg", mac1)
	create_mapping(str(uuid.uuid4()), "Engg", mac2)
	create_intent(str(uuid.uuid4()), "Mktg", "Engg", "allow")
	create_intent(str(uuid.uuid4()), "Engg", "Mktg", "allow")

	print_mappings()
	print_intents()

	delete_mappings()
	delete_intents()