import aprslib
import logging
import requests
import json

webhook = "WEBHOOK_URL_HERE"

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
    if "message_text" in packet:
        if "DCRDGTE" in packet['message_text']:
            print(packet)
            send_discord_message(webhook, "DCRDGTE", f"{packet['from']}:{packet['message_text'].replace('DCRDGTE','')}")

send_discord_message(webhook, "DCRDGTE", f"Ready to receive!")
AIS = aprslib.IS("N0CALL", "-1", "rotate.aprs2.net")
AIS.connect()
# by default `raw` is False, then each line is ran through aprslib.parse()
AIS.consumer(callback, raw=False)