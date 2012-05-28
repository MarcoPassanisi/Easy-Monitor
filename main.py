#!/usr/bin/env python

#-------------------------------------------------
# IMPORT
#-------------------------------------------------

import webapp2
import config
import controllers
from models import *
import jinja2
import os

#-------------------------------------------------
# TEMPLATE
#-------------------------------------------------

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#-------------------------------------------------
# MAIN PROGRAM
#-------------------------------------------------

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'url_check': controllers.urlCheck(),
            'last_status': controllers.lastStatus()
        }

        template = jinja_environment.get_template('views/index.html')
        self.response.out.write(template.render(template_values))

#-------------------------------------------------
# About Page
#-------------------------------------------------

class About(webapp2.RequestHandler):
    def get(self):
	title =  "About"
        template_values = {
            'title': title
        }

        template = jinja_environment.get_template('views/about.html')
        self.response.out.write(template.render(template_values))

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
                                ('/cron', Cron),
                                ('/about', About)
                               ],
                              debug=True)
