from google.appengine.ext import db

class Report(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty()