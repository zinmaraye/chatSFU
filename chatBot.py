# Import required libraries
import os
import sys
import json
from datetime import datetime, timedelta
import requests
from flask import Flask, request

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "isp_chat_bot_db",
}

AccessToken = "EAADrEJwQKy4BO3DTLwl4LpZAxjomGPu9J5XaDlP9PXlq9XVLz8wYGhTnqbZAAJ30CONCBS62Tz2fF3HB2Ckxd3nGRqXO4aZAoJOSDC8FhUgDiMY6iJcaKwrujjBKUcr9NTNXkmeRqn7A28Ilz4WxQAQXlZBJ0lMnPOhTPN3IYVZArD084Vj6sPubbpRULzV9F"

@app.route('/', methods=['GET'])
def fbverify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "abk":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200
@app.route('/', methods=['POST'])

def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # log for incoming message just for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    try:
                        message_text = messaging_event["message"]["text"]  # the message's text

                        process_reply_customer(sender_id, message_text)

                    except:
                        pass

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def process_reply_customer(sender_id, sender_text):

        if sender_text.lower() == "products":
            send_message(sender_id, "Here are category you might interest")
            send_message(sender_id, "Type: Id to check what products are available")

        elif sender_text.lower() == "buy":
            send_message(sender_id, "Type: Product Id of your wanted product")
               
        elif sender_text.lower() == "search":
            send_message(sender_id, "Type: product Id")
            
        elif sender_text.lower() == "staff":
            send_message(sender_id, "Staff will reply in few hour")

        elif sender_text.lower() == "help":
            send_message(sender_id, "Type: 'products' for products informations")
            send_message(sender_id, "Type: 'Search' for search products with ID")
            send_message(sender_id, "Type: 'buy' for buying products")
            send_message(sender_id, "Type: 'staff' to talk with our staff")

def send_message(recipient_id, message_text, image_url=None):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": AccessToken
    }
    headers = {
        "Content-Type": "application/json"
    }

    if image_url:
        data = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": image_url,
                        "is_reusable": True
                    }
                }
            }
        }
    else:
        data = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, json=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(msg, *args, **kwargs):
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = str(msg)  # Convert to string if not already
            if args or kwargs:
                msg = msg.format(*args, **kwargs)
        print("{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()

if __name__ == '__main__':
    print("Starting check_inactive_users process...")
    # Start the inactivity checker as a separate process
    print("check_inactive_users process started.")

    # Run the Flask app in the main thread
    app.run(debug=True, host="0.0.0.0", port="3000")