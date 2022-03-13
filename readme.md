# brightspace-decsync

utility that converts brightspace calendar events to decsync tasks

## dependencies

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## config.json

```
{
  "decsync": {
    "dir": "<decsync dir>",
    "collection": "<collection uuid for tasks>"
  },
  "brightspace": "<brightspace calendar id w/ token url argument>"
}
```
