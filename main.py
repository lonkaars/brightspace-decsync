#!/bin/python3

from libdecsync import Decsync
from icalendar import Calendar, Event
from taggen import tag_gen
from datetime import datetime
from uuid import uuid4
import time
import json
import os
import requests

APPID = "brightspace-decsync"

def load_config():
	config_file = open("./config.json", "r")
	config_json = json.loads(config_file.read())
	config_json["decsync"]["dir"] = os.path.expanduser(config_json["decsync"]["dir"])
	return config_json

def get_brightspace_events(config):
	request = requests.get(config["brightspace"])
	cal = Calendar.from_ical(request.text)
	return list(cal.walk('vevent'))

def create_task_ical(cal_event):
	cal = Calendar()
	event = Event()
	cal.add('prodid', APPID)
	cal.add('version', '2.0')

	event.add("priority", 9)
	event.add("status", "needs-action")

	tag = tag_gen(cal_event.get('location'))
	if tag: event.add("categories", tag)

	event.add("created", datetime.now())

	event.add("dtstamp", str(cal_event.get('dtstart'), 'utf-8'))
	event.add("uid", uuid4())

	event.add("summary", str(cal_event.get('summary'), 'utf-8'))
	event.add("description", str(cal_event.get('description'), 'utf-8'))
	cal.add_component(event)
	return cal.to_ical()

def task_handler(config, ds, event):
	epoch = time.time()
	timestamp = f"{int(epoch)}{int((epoch % 1) * 10 ** 9)}"
	ds.set_entry(["resources", timestamp], None, create_task_ical(event))

def main():
	config = load_config()
	ds = Decsync(config["decsync"]["dir"], "tasks", config["decsync"]["collection"], APPID)
	events = get_brightspace_events(config)
	for event in events:
		task_handler(config, ds, event)

if __name__ == "__main__":
	main()
