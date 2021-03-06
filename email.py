import smtplib
import ssl
import json
import csv
import pathlib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

f = open(str(pathlib.Path(__file__).parent.resolve())+ "/config.json")
config = json.loads(f.read())
f.close()

def login(s, email, password):
    s.ehlo()  # Can be omitted
    s.starttls(context=ssl.create_default_context())
    s.ehlo()
    s.login(email, password)

def createmsg(subject, sender, parts, osloveni):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    for x in parts:
        msg.attach(MIMEText(load_file(x["file"]).format(osloveni=osloveni),x["mime"]))
    return msg

def load_file(filename):
    fp = open(str(pathlib.Path(__file__).parent.resolve()) + "/" + filename)
    text = fp.read()
    fp.close()
    return text

s = smtplib.SMTP(host=config["mailserver"], port=config["mailserverport"], timeout=4.4)

login(s, config["sender"], config["password"])

with open(str(pathlib.Path(__file__).parent.resolve())+"/"+config["csv"], newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        msg = createmsg("test", config["sender"], config["emailparts"], row[1])
        msg["to"] = row[0]
        s.send_message(msg)

s.quit()