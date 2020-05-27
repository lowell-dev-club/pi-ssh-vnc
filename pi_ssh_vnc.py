# Imports
from re import findall
from time import sleep as delay
from config import *
from socket import gethostname
from smtplib import SMTP
from requests import get
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Request until ngrok is online
while True:

    delay(5)
    
    # request ngrok's local debug api
    tunnels = get('http://127.0.0.1:4040/api/tunnels')
    if tunnels.status_code == 200:
        break

# Get all the active tunnels from json
jsonTunnels = tunnels.json()['tunnels']

# Sort by the local port
jsonTunnels.sort(key=lambda tunnels: findall('[0-9]+', repr(tunnels['config']['addr']))[0])

email_message = ''

# Loop for every tunnel
for jsonItems in jsonTunnels:

    # Find the forwarded port of the current tunnel
    whichPort = findall('[0-9]+', repr(jsonItems['config']['addr']))[0]

    # Find the ngrok public url
    ngrokUrl = jsonItems['public_url']

    # If ssh
    if int(whichPort) == 22:

        # find the 0.tcp.ngrok.io port that forwards to local ssh port
        ngrokPort = findall('[0-9]+', repr(ngrokUrl))[1]
        email_message += (f'Port {whichPort} forwards to > 0.tco.ngrok.io port: {ngrokPort}\n')
        email_message += (f'VNC: \nssh -L 5900:localhost:5900 pi@0.tcp.ngrok.io -p {ngrokPort}\n')
        email_message += (f'SSH/TERMINAL: \nssh pi@0.tcp.ngrok.io -p {ngrokPort}\n\n')

    else:

        email_message += (f'Port {whichPort} forwards to > {ngrokUrl}\n\n')

# Find the computer hostname
hostname = repr(gethostname())

email_message += 'for\n'
email_message += hostname[1:len(hostname) - 1]

# Setup email message
name = ('pi-ssh-vnc <' + emailUser + '>')
msg = MIMEMultipart()
msg['From'] = name
msg['To'] = emailUser
msg['Subject'] = hostname[1:len(hostname) - 1] + ' was restarted, here are the new generated ngrok urls'
msg.attach(MIMEText(email_message,'plain'))
message = msg.as_string()

# Send email
smtp_server = SMTP('smtp.gmail.com', 587)
smtp_server.ehlo_or_helo_if_needed()
smtp_server.starttls()
smtp_server.ehlo_or_helo_if_needed()
smtp_server.login(emailUser, emailPass)
smtp_server.sendmail(emailUser, emailUser, message)
smtp_server.quit()