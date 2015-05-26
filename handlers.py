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

OAUTH_CLIENTID = "276925555487-ddj29ujtf20e2sljoarktk4cccjikgf3.apps.googleusercontent.com"
OAUTH_CLIENTSECRET = "iljnKdWzMB2ksu2VQC9at4rT"

class Handler(webapp2.RequestHandler):
    """Handler
        This handler will be the base of all Handlers.
        This handler will also define function `render`, that will render jinja templates
    """
    
    def __init__(self, request, response):
        self.initialize(request, response)
        self.sys = SY.query()
        self.teachers = Teacher.query()
        self.classes = Classes.query()

    def write(self, *a, **kw):
        """Helper function for rendering htmls"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Helper function for rendering htmls"""

        t = JINJA.get_template(template)
        return t.render(params)

    def render(self, tempalte, **kw):
        """This will render an html from a template with the given keywords
        Parameters:
            template (str): a string where the file template is found. location
            `title` keyword should always be defined.
            **kw: keywords that will be used by the template
        """
        self.write(self.render_str(tempalte, **kw))

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
