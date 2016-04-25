from flask import Flask, request, render_template as render
from twilio.rest import TwilioRestClient
import twilio.twiml
from os import environ as env

SID = env.get('SID', None)
TKN = env.get('TKN', None)
DMN = env.get('DMN', None)
FRM = env.get('FRM', None)

app = Flask(__name__)
client = TwilioRestClient(SID, TKN)

@app.route("/")
def index():
    return "Nothing to see here ;)"

@app.route("/sms/reply", methods=["POST"])
def sms_reply():
    message = ""

    from_number = request.values.get('From', None)
    to_number = request.values.get('To', None)
    body = request.values.get('Body', None)

    if str(body).strip().lower() == "settings":
        message = "To change your settings tap %s/settings" % DMN
    elif str(body).strip().lower() == "hi":
        message = "Hi! What can we help you with? %s/hi" % DMN
    else:
        message = """From: %s, To: %s Body: %s""" % (from_number, to_number, body)

    client.messages.create(
        body=message,
        to=from_number,
        from_=FRM
    )

    return "OK"

@app.route("/settings")
def settings():
    return render('settings.html')

@app.route("/hi")
def hi():
    return render('hi.html')

if __name__=='__main__':
    app.run(debug=True)
