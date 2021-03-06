import os
import sys
import json
from datetime import datetime

#from tzlocal import get_localzone

import requests
from flask import Flask, request

import urllib

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    send_message(sender_id, "roger that!")
                    #send_message(sender_id, "bob that!")
                    
                    apiKey = 'S1AKS2D2LNU9PY5L'
                    #noKeyURL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=&interval=1min&apikey='
                    #apiIndex = line.find('apikey=')
                    #keyURL = noKeyURL[:apiIndex] + apiKey + noKeyURL[apiIndex:]
                    # place the symbol after symbol= and the apikey after apikey=
                    #send_message(sender_id, noKeyURL)

                        #now = datetime.now()
                        #hour = now.hour
                        #minute = now.minute
                        #year = now.year
                        #month = now.month
                        #day = now.day
                    
                        #completeDate = "{}-{}-{}".format(year, month, day)
                        
                    #symbol = message_text.split("$")
                    if "$" in message_text:
                        #send_message(sender_id, message_text)
                        hardParse = message_text[1:]
                        #send_message(sender_id, hardParse)
                        
                        theURL = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=1min&apikey={}".format(hardParse, apiKey)
               
                        response = urllib.urlopen(theURL)
                        dataDict = json.loads(response.read())
                        
                        #send_message(sender_id, "roger that!")                     
                        #send_message(sender_id, data)
                       
                        now = datetime.now()
                        
                        hour = now.hour
                        minute = now.minute
                        year = now.year
                        month = now.month
                        day = now.day
                        
                        #send_message(sender_id, str(type(hour)))
                    
                        if 0 <= hour and hour < 5 :
                            hour = 24 + hour - 5
                            day = day - 1
                        else:
                            hour = hour - 5
                    
                        completedDate = "{}-{}-{}".format(year, month, day)
                        completedTime = "{}:{}:00".format(hour, minute)
                        timeStamp = "{} {}".format(completedDate, completedTime)
                        
                        #currentTime = now.strftime("%Y-%m-%d %H:%M")
                        #rightNow = "{}:00".format(currentTime)
                        #tz = get_localzone()
                        
                        send_message(sender_id, "EST Time: ")
                        #send_message(sender_id, str(now))
                        #send_message(sender_id, completeDate)
                        #send_message(sender_id, completeTime)
                        send_message(sender_id, timeStamp)

                        #send_message(sender_id, str(now.hour))
                        #send_message(sender_id, str(now.minute))

                        #send_message(sender_id, str(datetime.today()))  
                        #symbolIndex = line.find('symbol=')
                        #symbolURL = keyURL[:symbolIndex] + hardParse + keyURL[symbolIndex:]
                        #send_message(sender_id, symbolURL)
                        
                        completeDate = sorted(dataDict["Time Series (1min)"].keys())[-1]
                        send_message(sender_id, "Last Trade Info: ")
                        send_message(sender_id, completeDate)
                        smallDict = dataDict["Time Series (1min)"][completeDate]
                        for key in sorted(smallDict.keys()):
                            send_message(sender_id, ("{} {}".format(key, smallDict[key])))

                        
                    elif "!" in message_text:
                        #send_message(sender_id, message_text)
                        hardParse = message_text[1:]
                        #send_message(sender_id, hardParse)
                        
                        theURL = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={}&market=EUR&apikey={}".format(hardParse, apiKey)
               
                        response = urllib.urlopen(theURL)
                        dataDict = json.loads(response.read())
                        
                        #send_message(sender_id, "roger that!")                     
                        #send_message(sender_id, data)
                       
                        now = datetime.now()
                        
                        hour = now.hour
                        minute = now.minute
                        year = now.year
                        month = now.month
                        day = now.day
                        
                        #send_message(sender_id, str(type(hour)))
                    
                        if 0 <= hour and hour < 5 :
                            hour = 24 + hour - 5
                            day = day - 1
                        else:
                            hour = hour - 5
                    
                        completedDate = "{}-{}-{}".format(year, month, day)
                        completedTime = "{}:{}:00".format(hour, minute)
                        timeStamp = "{} {}".format(completedDate, completedTime)
                        
                        #currentTime = now.strftime("%Y-%m-%d %H:%M")
                        #rightNow = "{}:00".format(currentTime)
                        #tz = get_localzone()
                        
                        send_message(sender_id, "EST Time: ")
                        #send_message(sender_id, str(now))
                        #send_message(sender_id, completeDate)
                        #send_message(sender_id, completeTime)
                        send_message(sender_id, timeStamp)
                        
                        #send_message(sender_id, theURL)
                        send_message(sender_id, completedDate)
                        
                        completeDate = sorted(dataDict["Time Series (Digital Currency Daily)"].keys())[-1]
                        smallDict = dataDict["Time Series (Digital Currency Daily)"][completeDate]
                        for key in sorted(smallDict.keys()):
                            send_message(sender_id, ("{} {}".format(key, smallDict[key])))
                    
                    elif "S&P" in message_text or "s&p" in message_text:
                        
                        theURL = "https://www.alphavantage.co/query?function=SECTOR&apikey={}".format(apiKey)
                        response = urllib.urlopen(theURL)
                        dataDict = json.loads(response.read())
                       
                        now = datetime.now()
                        
                        hour = now.hour
                        minute = now.minute
                        year = now.year
                        month = now.month
                        day = now.day
                        
                        #send_message(sender_id, str(type(hour)))
                    
                        if 0 <= hour and hour < 5 :
                            hour = 24 + hour - 5
                            day = day - 1
                        else:
                            hour = hour - 5
                    
                        completedDate = "{}-{}-{}".format(year, month, day)
                        completedTime = "{}:{}:00".format(hour, minute)
                        timeStamp = "{} {}".format(completedDate, completedTime)
                        
                        send_message(sender_id, "S and P Performance By Sector")

                        send_message(sender_id, "EST Time: ")
                        send_message(sender_id, timeStamp)
                        
                        #completeDate = sorted(dataDict["Time Series (1min)"].keys())[-1]
                        send_message(sender_id, "Real Time Performance: ")
                        send_message(sender_id, completeDate)
                        smallDict = dataDict["Rank A: Real-Time Performance"]
                        for key in smallDict.keys():
                            send_message(sender_id, key)
                            send_message(sender_id, ("{} {}".format(key, smallDict[key])))
                        
                        send_message(sender_id, "Year to Date Performance: ")
                        send_message(sender_id, completeDate)
                        smallDict = dataDict["Rank F: Year-to-Date (YTD) Performance"]
                        for key in smallDict.keys():
                            send_message(sender_id, ("{} {}".format(key, smallDict[key])))
                    
                    else:
                        send_message(sender_id, "nope")
                    
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
