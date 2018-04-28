import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.westwin.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login("feisun@westwin.com", "Bingart975")

fromaddr = "feisun@westwin.com"
toaddr = "feisun@westwin.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Python email"
body = "Python test mail"
msg.attach(MIMEText(body, 'plain'))

text = msg.as_string()
server.sendmail("feisun@westwin.com", "feisun@westwin.com", text)