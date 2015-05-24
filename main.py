#!/usr/bin/env python


import webapp2
from handlers import *
from models import *

class Home(Handler):
    def get(self):
        self.render("home.html", title="Teacher's Sched Maker")


app = webapp2.WSGIApplication([
    ('/', Home)
], debug=True)
