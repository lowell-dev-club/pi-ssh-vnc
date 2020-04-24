import requests
import socket
from config import *
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

time.sleep(60 * 3)


tunnels = requests.get('http://127.0.0.1:4040/api/tunnels')
jsonTunnels = tunnels.json()['tunnels']

email_message = ''

for jsonItems in jsonTunnels:
    email_message += (jsonItems['config']['addr'] + '\n')
    email_message += (jsonItems['public_url']) + '\n\n'

hostname = repr(socket.gethostname())

email_message += 'for\n'
email_message += hostname

name = ('pi-ssh-vnc <' + emailUser + '>')
msg = MIMEMultipart()
msg['From'] = name
msg['To'] = emailUser
msg['Subject'] = hostname + ' was restarted, here are the new generated ngrok urls'
msg.attach(MIMEText(email_message,'plain'))
message = msg.as_string()

smtp_server = SMTP('smtp.gmail.com', 587)
smtp_server.ehlo_or_helo_if_needed()
smtp_server.starttls()
smtp_server.ehlo_or_helo_if_needed()
smtp_server.login(emailUser, emailPass)
smtp_server.sendmail(emailUser, emailUser, message)
smtp_server.quit()