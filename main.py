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
        
        self.next("sy?id="+str(sy.id()))

class viewSY(Handler):
    def get(self):
        sy = SY.get_by_id(int(self.request.get('id')))
        self.render("sy.html",
                    sy = sy,
                    sys = self.sys,
                    teachers = Teacher.query(ancestor = sy.key),
                    levels = self.getLevels(sy))

class NewClass(Handler):
    def get(self):
        sy = SY.get_by_id(int(self.request.get('id')))
        self.render("new-class.html", 
                    sy = sy,
                    sys = self.sys,
                    teachers = Teacher.query(ancestor=sy.key),
                    levels = self.getLevels(sy))

    def post(self):
        sy = SY.get_by_id(int(self.request.get('id')))
        name = self.request.get('name')
        level = int(self.request.get('lvl'))
        adviser = self.request.get('adviser')
        if adviser:
            newClass = Class(parent=sy.key, name=name, level=level, adviser=int(adviser)).put()
        else:
            newClass = Class(parent=sy.key, name=name, level=level).put()
        self.next('class?id='+str(newClass.id())+'&parent='+str(sy.key.id()))

class viewClass(Handler):
    def get(self):
        sy = SY.get_by_id(int(self.request.get('parent')))
        myclass = Class.get_by_id(int(self.request.get('id')), parent=sy.key)
        self.render("class.html",
                    sys = self.sys,
                    levels = self.getLevels(sy),
                    teachers = self.getTeachers(sy),
                    sy = sy,
                    myClass = myclass)

class NewTeacher(Handler):
    def get(self):
        sy = SY.get_by_id(int(self.request.get('id')))
        self.render("new-teachers.html",
                    sys = self.sys,
                    teachers = self.getTeachers(sy),
                    levels = self.getLevels(sy),
                    sy = sy)

    def post(self):
        sy = SY.get_by_id(int(self.request.get('id')))
        name = self.request.get("name")
        teacher = Teacher(name=name, parent=sy.key).put()
        self.next('teacher?id='+str(teacher.id())+'&parent='+str(sy.key.id()))

class viewTeacher(Handler):
    def get(self):
        sy = SY.get_by_id(int(self.request.get('parent')))
        teacher = Teacher.get_by_id(int(self.request.get('id')), parent = sy.key)
        self.render("teacher.html",
                    sys = self.sys,
                    teachers = self.getTeachers(sy),
                    levels = self.getLevels(sy),
                    sy = sy,
                    teacher = teacher)


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/new-sy', NewSY),
    ('/sy', viewSY),
    ('/new-class', NewClass),
    ('/class', viewClass),
    ('/new-teacher', NewTeacher),
    ('/teacher', viewTeacher)
], debug=True)
