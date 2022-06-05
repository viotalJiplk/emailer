import smtplib
import ssl
import json
import csv
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

f = open("email/config.json")
config = json.loads(f.read())
f.close()

def login(s, email, password):
    s.ehlo()  # Can be omitted
    s.starttls(context=ssl.create_default_context())
    s.ehlo()
    s.login(email, password)

def createmsg(subject, sender, parts):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    for x in parts:
        msg.attach(MIMEText(load_file(x["file"]),x["mime"]))
    return msg

def load_file(filename):
    fp = open(filename)
    text = fp.read()
    fp.close()
    return text

msg = createmsg("test", config["sender"], config["emailparts"])
emails = []

with open(config["csv"], newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        emails.append(row[0])

s = smtplib.SMTP(host=config["mailserver"], port=config["mailserverport"], timeout=4.4)

login(s, config["sender"], config["password"])
for email in emails:
    msg["to"] = email 
    s.send_message(msg)
s.quit()