import smtplib

TO = 'zhuoyan.li@nuance.com'
SUBJECT = 'TEST MAIL'
TEXT = 'Here is a message from python.'

# Gmail Sign In
gmail_sender = 'zhuoyan.li@gmail.com'
gmail_passwd = 'M@nL!925'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_sender, gmail_passwd)

BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])

try:
    server.sendmail(gmail_sender, [TO], BODY)
    print ('email sent')
except:
    print ('error sending mail')

server.quit()

