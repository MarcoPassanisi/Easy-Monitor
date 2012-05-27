from google.appengine.api import urlfetch
import config
from models import *
from google.appengine.api import mail

#-------------------------------------------------
# Function Url Check Status
#-------------------------------------------------

def urlCheck():
    """This function provide the website status in real time"""
    url_result = urlfetch.fetch(
                                config.URL,
                                payload=None,
                                allow_truncated=False,
                                follow_redirects=True,
                                deadline=10,
                                headers={'Cache-Control' : 'max-age=0'},
                                validate_certificate=None
                                )
    if url_result.status_code == 200 and url_result.content.find(config.SEARCH_STRING) != -1:
        site_status = ("UP")
    else:
        site_status = ("DOWN")
    return site_status

#-------------------------------------------------
# Function Last event put into datastore
#-------------------------------------------------

def lastStatus():
    """This function provide the last status event recorded into datastore"""
    q = Report.all()
    q.order("-date")
    result = q.fetch(limit=1)
    if len(result) == 0:
        last_status = None
    else:
        for s in result:
            last_status = s.status
    return last_status

#-------------------------------------------------
# Function Send Mail
#-------------------------------------------------

def sendMail(subject_status):
    """This function serve for send mail"""
    sender = config.SENDER
    to = config.TO
    subject = subject_status
    body = config.BODY
    return mail.send_mail(sender, to, subject, body)
    
    
    


        
