## Description

Smartscale powered by wii balance (wiiboard) using python on a Raspberry PI 2.

Stores weight data on sqlite3 database.

## Config

Some values have been hardcoded in `smartscale.py` like the user's name (by weight),
or the wiiboard MAC address (uncomment discover to find yours).

## Run

python smartscale.py

Then click on the red button below the wiiboard until the blue leds turns ON (stops flashing)

## Requirements

Install dependencies

```
sudo apt-get install libbluetooth-dev python-pygame

pip install -r requirements.txt
```

## DB schema

    CREATE TABLE IF NOT EXISTS balance (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp NUMERIC, weight NUMBER, user TEXT);

## BT Troubleshooting

If bluez can't connec to device: http://stackoverflow.com/questions/30321192/bluez-on-i-mx25-cant-connect-rfcomm-socket-operation-now-in-progress

Configure bluez client on debian: http://bediyap.com/linux/bluez-client-server-in-debian/

If server complains about not finding display, do `export DISPLAY=:0.0`
