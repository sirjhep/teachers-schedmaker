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

class viewSY(Handler):
    def get(self, syid):
        sy = SY.get_by_id(int(syid))
        self.render("sy.html",
                    sy = sy,
                    sys = self.sys)

class NewSection(Handler):
    def get(self, syid):
        sy = SY.get_by_id(int(syid))
        self.render("new-section.html", 
                    sy = sy,
                    sys = self.sys)

class NewTeacher(Handler):
    def get(self, syid):
        sy = SY.get_by_id(int(syid))
        self.render("new-teachers.html",
                    sy = sy,
                    sys = self.sys)

    def post(self, syid):
        sy = SY.get_by_id(int(syid))
        name = self.request.get("name")
        teacher = Teacher(name=name, parent=sy.key).put()
        self.next('/teacher/'+str(sy)+'/teacher/'+str(teacher.id()))

class viewTeacher(Handler):
    def get(self, syid, tid):
        sy = SY.get_by_id(int(syid))
        teacher = Teacher.get_by_id(int(tid))
        self.render("teacher.html",
                    sy = sy,
                    teacher=teacher,
                    sys = self.sys)

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/new-sy', NewSY),
    ('/sy/(\d+)?', viewSY),
    ('/teacher/(\d+)?', viewTeacher),
    ('/sy/(\d+)?/new-section', NewSection),
    ('/sy/(\d+)?/new-teacher', NewTeacher),
    ('/sy/(\d+)?/teacher/(\d+)?', viewTeacher)
], debug=True)
