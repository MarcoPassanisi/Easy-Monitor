#!/usr/bin/env python

#-------------------------------------------------
# IMPORT
#-------------------------------------------------

import webapp2
import config
import controllers
from models import *

#-------------------------------------------------
# MAIN PROGRAM
#-------------------------------------------------

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Easy Monitor, status website: ' +  controllers.urlCheck() + " - " + "Last Status: ")
        self.response.out.write(controllers.lastStatus())

#-------------------------------------------------
# CRON
#-------------------------------------------------

class Cron(webapp2.RequestHandler):
    def get(self):
        if controllers.urlCheck() == "UP" and controllers.lastStatus() == "down" or controllers.lastStatus() == None:
            Report(status = "up").put()
            controllers.sendMail(config.SUBJECT_STATUS_UP)
        elif controllers.urlCheck() == "UP" and controllers.lastStatus() == "up":
            pass
        elif controllers.urlCheck() == "DOWN" and controllers.lastStatus() == "up" or controllers.lastStatus() == None:
            Report(status = "down").put()
            controllers.sendMail(config.SUBJECT_STATUS_DOWN)
        elif controllers.urlCheck() == "DOWN" and controllers.lastStatus() == "down":
            pass

        return webapp2.redirect('/')

#-------------------------------------------------
# ROUTING
#-------------------------------------------------

app = webapp2.WSGIApplication([
                                ('/', MainPage),
                                ('/cron', Cron)
                               ],
                              debug=True)
