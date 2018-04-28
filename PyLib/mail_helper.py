# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailHelper:
    
    def __init__(self, smtpHost, userAddress, userPassword, port = 25):
        self._smtpHost = smtpHost
        self._userAddress = userAddress
        self._userPassword = userPassword
        self._port = port
        self._server = smtplib.SMTP(self._smtpHost, self._port)
        try:
            self._server.ehlo()
            self._server.starttls()
            self._server.ehlo()
        except Exception as err :
            print(err)
        self._server.login(self._userAddress, self._userPassword)

    def close(self):
        self._server.quit()
        
    def pushMail(self, theFrom, theTo, subject, body):
        msg = MIMEMultipart()
        msg['From'] = theFrom
        msg['To'] = theTo
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        text = msg.as_string()
        self._server.sendmail(theFrom, theTo, text)

    
    def pushHtmlMail(self, theFrom, theTo, subject, html):
        msg = MIMEMultipart('alternative')
        msg['From'] = theFrom
        msg['To'] = theTo
        msg['Subject'] = subject

        # Record the MIME types of both parts - text/plain and text/html.
        # part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        # msg.attach(part1)
        msg.attach(part2)
        self._server.sendmail(theFrom, theTo, msg.as_string())
    
    def pushHtmlMailList(self, theFrom, theToList, subject, html):
        msg = MIMEMultipart('alternative')
        msg['From'] = theFrom
        msg['To'] = theToList[0]
        msg['Subject'] = subject

        # Record the MIME types of both parts - text/plain and text/html.
        # part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        # msg.attach(part1)
        msg.attach(part2)
        self._server.sendmail(theFrom, theToList, msg.as_string())
    
if __name__=="__main__":
    print("main")
    
    if False:
        helper = MailHelper('smtp.westwin.com', "feisun@westwin.com", "Bingart503", 587)
        theFrom = "feisun@westwin.com"
        theTos = ["feisun@westwin.com", "feisun@westwin.com"]
        theTos = ["feisun@westwin.com"]
        subject = "P123 Crawling Report"
        body = "test mail"
        for theTo in theTos:
            try:
                #helper.pushMail(theFrom, theTo, subject, body)
                print ("skip")
            except Exception as err :
                print(err)
        print("exit")
        helper.close()
    
    if True:
        helper = MailHelper('smtp.mail.healthtopquestions.com', "newsletter@mail.healthtopquestions.com", "Bingart503")
        theFrom = "newsletter@mail.healthtopquestions.com"
        theTos = ["feisun@westwin.com"]
        text = 'healthtopquestions.com newsletter 2018-04-09'
        html = """\
            <html>
            <head></head>
            <body>
            </body>
            </html>
            """
        html = """\
<a href="http://healthtopquestions.com/constipation-related-to-irritable-bowel-syndrome/">Is Constipation Related to Irritable Bowel Syndrome (IBS)?</a>
        """
        for theTo in theTos:
            try:
                helper.pushHtmlMail(theFrom, theTo, text, html)
            except Exception as err :
                print(err)
            print("exit")
        helper.close()
