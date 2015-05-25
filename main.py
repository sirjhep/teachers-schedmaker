#!/usr/bin/env python


import webapp2
from handlers import *
from models import *

class Home(Handler):
    def get(self):
        self.render("home.html",
                    title="Teacher's Sched Maker",
                    sys = self.sys)

class NewSY(Handler):
    def get(self):            
        self.render("new-sy.html",
                    title="Add new School Year",
                    sys = self.sys)
        
    def post(self):
        startyr = self.request.get("startyr")
        endyr = self.request.get("endyr")
        school_name = self.request.get("schoolname")
        
        if school_name:
            sy = SY(startyr=startyr,
                    endyr=endyr,
                    school_name=school_name).put()
        else:
            sy = SY(startyr=startyr,
                    endyr=endyr).put()
        
        self.next("sy/"+str(sy.id()))


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/new-sy', NewSY)
], debug=True)
