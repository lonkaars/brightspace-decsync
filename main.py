#!/bin/python3

from libdecsync import Decsync
from icalendar import Calendar, Todo
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

def create_task_ical(event):
  cal = Calendar()
  todo = Todo()
  cal.add('prodid', APPID)
  cal.add('version', '2.0')

  todo.add("priority", 9)
  todo.add("status", "needs-action")

  tag = tag_gen(event.get('location'))
  if tag: todo.add("categories", [tag])

  todo.add("created", datetime.now())

  todo.add("dtstamp", event.decoded('dtstart'))
  todo.add("uid", uuid4())

  todo.add("summary", event.decoded('summary'))
  description = event.get('description')
  if description: todo.add("description", description)

  cal.add_component(todo)
  return cal.to_ical()

def task_handler(config, ds, event):
  epoch = time.time()
  timestamp = f"{int(epoch)}{int((epoch % 1) * 10 ** 9)}"
  ds.set_entry(["resources", timestamp], None, str(create_task_ical(event), 'utf-8'))

def main():
  config = load_config()
  ds = Decsync(config["decsync"]["dir"], "tasks", config["decsync"]["collection"], APPID)
  events = get_brightspace_events(config)
  for event in events:
    task_handler(config, ds, event)

if __name__ == "__main__":
  main()
