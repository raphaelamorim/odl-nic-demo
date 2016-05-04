#!/usr/bin/python
__author__ = "Cris Shumate"

import nic_api as nic
import uuid
import sys
import os

def test_demo():
	nic.demo()

def help(cmd):
	if cmd == "all":
		print "\nUsage: <> required, [] optional"

		print "------"

		print "  map <epg> to <domain> [uid]"
		print "  intent <epg1> to <epg2> <action> [uid]"
		print "  print <objects>"
		print "  delete <objects>"

		print "------\n"
	elif cmd == "map":
		print "  map <epg> to <domain> [uid]\n"
	elif cmd == "intent":
		print "  intent <epg1> to <epg2> <action> [uid]\n"
	elif cmd == "print":
		print "  print <mappings | intents>\n"
	elif cmd == "delete":
		print "  delete <mappings | intents>\n"

def mapping(cmds):	
	if len(cmds) != 4 and len(cmds) != 5:
		help("map")
		return

	uid = ""
	
	if len(cmds) == 4:
		uid = str(uuid.uuid4())
	else:
		uid = cmds[4]

	nic.create_mapping(uid, cmds[1], cmds[3])

def intent(cmds):
	if len(cmds) != 5 and len(cmds) != 6:
		help("intent")
		return

	uid = ""

	if len(cmds) == 5:
		uid = str(uuid.uuid4())
	else:
		uid = cmds[5]

	nic.create_intent(uid, cmds[1], cmds[3], cmds[4])

def nic_print(cmds):
	if len(cmds) != 2:
		help("print")
		return

	if cmds[1] == "mappings":
		nic.print_mappings()
	elif cmds[1] == "intents":
		nic.print_intents()
	else:
		help("print")

def delete(cmds):
	if len(cmds) != 2:
		help("delete")
		return

	if cmds[1] == "mappings":
		nic.delete_mappings()
	elif cmds[1] == "intents":
		nic.delete_intents()
	else:
		help("delete")

def import_mappings():
	mappings = 0

	try:
		mappings = open("mappings.nic", "r")
	except IOError:
		print "error opening mappings file"
		return

	maps = mappings.readlines()

	cmd = ["map"]
	for m in maps:
		cmds = m.split()
		mapping(cmd + cmds)

def import_intents():
	intents = 0

	try:
		intents = open("intents.nic", "r")
	except IOError:
		print "error opening intents file"
		return

	intent_list = intents.readlines()

	cmd = ["intent"]
	for i in intent_list:
		cmds = i.split()
		intent(cmd + cmds)

def main():
	if os.path.isfile("mappings.nic"):
		resp = raw_input("\nA mappings file was detected, would you like to import the mappings? [y/n]: ")
		resp = resp.lower()

		if resp == "y" or resp == "yes":
			import_mappings()

	if os.path.isfile("intents.nic"):
		resp = raw_input("\nAn intents file was detected, would you like to import the intents? [y/n]: ")
		resp = resp.lower()

		if resp == "y" or resp == "yes":
			import_intents()

	print

	while True:
		cmd = raw_input("nic> ")

		if len(cmd) == 0:
			help("all")
			continue

		cmds = cmd.split()
		cmd = cmds[0]

		if cmd == "exit" or cmd == "quit" or cmd == "shutdown":
			print 'exiting\n'
			return
		elif cmd == "map":
			mapping(cmds)
		elif cmd == "intent":
			intent(cmds)
		elif cmd == "print":
			nic_print(cmds)
		elif cmd == "delete":
			delete(cmds)
		else:
			help("all")

main()