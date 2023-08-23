import aprslib
import logging
import requests
import json
import configparser

# Create a new configparser object
config = configparser.ConfigParser()
config.read('config.ini')

webhook = config['dcdgte']['WEBHOOK_URL']

def send_discord_message(webhook_url, sender, message):
    payload = {
        "username": sender,
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code != 204:
        print("Failed to send Discord message:", response.text)

def callback(packet):
    if "addresse" in packet:
        if "DCDGTE" in packet['addresse']:
            print(packet)
            send_discord_message(webhook, "DCDGTE", f"{packet['from']}: {packet['message_text']}")
            if "msgNo" in packet:
                print("Creating temporary connection")
                temp_AIS = aprslib.IS(config['dcdgte']['ACK_CALLSIGN'], host="rotate.aprs.net", port="14580", passwd=config['dcdgte']['ACK_PASSCODE'])
                temp_AIS.connect(blocking=True)
                print("Responding with ACK")
                ack_packet = f"DCDGTE>DCDGTE::{packet['from']}  :ack{packet['msgNo']}"
                print(ack_packet)
                temp_AIS.sendall(ack_packet)
                print("Closing temporary connection")
                temp_AIS.close()

print("Setting login...")
AIS = aprslib.IS("N0CALL", host="rotate.aprs.net", port="14580", passwd="-1")
print("Logged in...")
AIS.set_filter("t/m")
print("Filter set...")
AIS.connect()
print("Connected...")
# by default `raw` is False, then each line is ran through aprslib.parse()
AIS.consumer(callback, raw=False)