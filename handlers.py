import webapp2
import json
import os
import jinja2
import urllib, urllib2
from google.appengine.api import users
from models import *

TEMP_DIR = os.path.join(os.path.dirname(__file__), 'htmls')

JINJA = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMP_DIR),
                       autoescape=True)

class Handler(webapp2.RequestHandler):
    """Handler
        This handler will be the base of all Handlers.
        This handler will also define function `render`, that will render jinja templates
    """
    
    def __init__(self, request, response):
        self.initialize(request, response)
        self.sys = SY.query()
        id_get = self.request.get('id')
        parent_get = self.request.get('parent')
        self.sy = False
        self.myclass = False
        self.levels = False
        self.teacher = False
        self.teachers = False
        if self.request.path in ['/', '/sy', '/new-teacher', 'new-class'] and id_get:
            self.sy = SY.get_by_id(int(id_get))
        elif self.request.path in ['/class', '/teacher'] and parent_get:
            self.sy = SY.get_by_id(int(parent_get))
        if self.sy:
            self.levels = self.getLevels(self.sy)
            self.teachers = Teacher.query(ancestor=self.sy.key)
            if self.request.path == '/class':
                self.myclass =  Class.get_by_id(int(id_get), parent=self.sy.key)
            elif self.request.path == '/teacher' and id_get:
                self.teacher = Teacher.get_by_id(int(id_get), parent=self.sy.key)

    def write(self, *a, **kw):
        """Helper function for rendering htmls"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Helper function for rendering htmls"""

        t = JINJA.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """This will render an html from a template with the given keywords
        Parameters:
            template (str): a string where the file template is found. location
            `title` keyword should always be defined.
            **kw: keywords that will be used by the template
        """
        kws = {'sys': self.sys,
              'sy': self.sy,
              'levels': self.levels,
              'teachers': self.teachers,
              'Class': self.myclass,
              'teacher': self.teacher}
        kws.update(**kw)
        self.write(self.render_str(template, **kws))

    def next(self, url):
        """This will replace the usual redirect method, whereas the redirection will now be conditional depending if  the user is login or not. Use this instead of ``.redirect``
        Parameters:
        url (str): Not the whole url, just the url that is defined on the bottom of this module.
       """
        self.redirect('/' + str(url))
    
    def writeJSON(self, adict):
        """respond with a json content-type, converting a dictionary type to json"""
        self.response.headers["Content-Type"] = "text/json"
        self.write(json.dumps(adict))
 
    def log(self, message):
        """
        Creates a log script that logs it to the browsers log.
        Parameters:
            self (Handler): a webapp2.RequestHandler class
            message (str): the message to be log.
        TODO: replace this to be a log file instead of output on browser.
        """
        self.write("<script>console.log('" + message + "');</script>")

    def getLevels(self, sy):
        levels = {}
        for i in range(0, 13):
            fori = Class.query(ancestor = sy.key, filters=(Class.level == i))
            if fori.count() is not 0:
                levels[i]=fori
        return levels