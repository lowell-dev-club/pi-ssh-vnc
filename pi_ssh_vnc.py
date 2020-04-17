import requests
import socket
from config import *
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


tunnels = requests.get('http://127.0.0.1:4040/api/tunnels')
jsonTunnels = tunnels.json()['tunnels']

email_message = ''

for jsonItems in jsonTunnels:
    email_message += (jsonItems['public_url']) + '\n'

email_message += socket.gethostname()

name = ('pi-ssh-vnc <' + emailUser + '>')
msg = MIMEMultipart()
msg['From'] = name
msg['To'] = emailUser
msg['Subject'] = 'A pi was restarted, here are the newley generated ngrok urls'
msg.attach(MIMEText(email_message,'plain'))
message = msg.as_string()

smtp_server = SMTP('smtp.gmail.com', 587)
smtp_server.ehlo_or_helo_if_needed()
smtp_server.starttls()
smtp_server.ehlo_or_helo_if_needed()
smtp_server.login(emailUser, emailPass)
smtp_server.sendmail(emailUser, emailUser, message)
smtp_server.quit()