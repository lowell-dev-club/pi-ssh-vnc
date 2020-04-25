import requests
import socket
from config import *
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import re

while True:
    time.sleep(5)
    tunnels = requests.get('http://127.0.0.1:4040/api/tunnels')
    if tunnels.status_code == 200:
        break

jsonTunnels = tunnels.json()['tunnels']

email_message = ''

for jsonItems in jsonTunnels:

    whichPort = re.findall('[0-9]+', repr(jsonItems['config']['addr']))[0]
    ngrokUrl = jsonItems['public_url']

    if int(whichPort) == 22:
        ngrokPort = re.findall('[0-9]+', repr(ngrokUrl)[1]
        email_message += (f'Port: {whichPort} forwards to > 0.tco.ngrok.io port: {ngrokPort}\n\n')
    else:
        email_message += (f'Port: {whichPort} forwards to > {ngrokUrl}\n\n')

hostname = repr(socket.gethostname())

email_message += 'for\n'
email_message += hostname[1:len(hostname) - 1]

name = ('pi-ssh-vnc <' + emailUser + '>')
msg = MIMEMultipart()
msg['From'] = name
msg['To'] = emailUser
msg['Subject'] = hostname[1:len(hostname) - 1] + ' was restarted, here are the new generated ngrok urls'
msg.attach(MIMEText(email_message,'plain'))
message = msg.as_string()

smtp_server = SMTP('smtp.gmail.com', 587)
smtp_server.ehlo_or_helo_if_needed()
smtp_server.starttls()
smtp_server.ehlo_or_helo_if_needed()
smtp_server.login(emailUser, emailPass)
smtp_server.sendmail(emailUser, emailUser, message)
smtp_server.quit()