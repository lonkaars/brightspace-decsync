#!/bin/python3

from libdecsync import Decsync
from icalendar import Calendar, Todo
from datetime import datetime
from uuid import uuid4
import filters
import time
import re
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

def description_parser(desc):
  return (re.sub(r'\n\nView event - (.+)', r'[view event](\1)', desc),
  re.sub(r'View event - (.+)', r'\1', desc))

def create_task_ical(event):
  cal = Calendar()
  todo = Todo()
  cal.add('prodid', APPID)
  cal.add('version', '2.0')

  todo.add("priority", 9)
  todo.add("status", "needs-action")

  tag = filters.tag_gen(event.get('location'))
  if tag: todo.add("categories", [tag])

  todo.add("created", datetime.now())
  todo.add("due", event.decoded('dtstart'))
  todo.add("summary", filters.title_filter(str(event.decoded('summary'), 'utf-8')))

  desctext = event.get('description')
  if not desctext: return None
  description, uid = description_parser(desctext)
  todo.add("description", description)
  todo.add("uid", uid)

  cal.add_component(todo)
  return (cal.to_ical(), uid)

def task_handler(config, ds, event):
  temp = create_task_ical(event)
  if not temp: return
  ical, uid = temp
  ds.set_entry(["resources", uid], str(event.decoded('uid'), 'utf-8'), str(ical, 'utf-8'))

def main():
  config = load_config()
  ds = Decsync(config["decsync"]["dir"], "tasks", config["decsync"]["collection"], APPID)
  events = get_brightspace_events(config)
  for event in events:
    task_handler(config, ds, event)

if __name__ == "__main__":
  main()
