#!/bin/python3

from libdecsync import Decsync
from icalendar import Calendar
from taggen import tag_gen
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

def task_handler(config, ds, event):
  epoch = time.time()
  timestamp = f"{int(epoch)}{int((epoch % 1) * 10 ** 9)}"
  print(timestamp)
  ds.set_entry(["resources", timestamp], None, "ical content here")

def main():
  config = load_config()
  ds = Decsync(config["decsync"]["dir"], "tasks", config["decsync"]["collection"], APPID)
  events = get_brightspace_events(config)
  for event in events:
    task_handler(config, ds, event)

if __name__ == "__main__":
  main()
