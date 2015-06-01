#!/usr/bin/env python


import webapp2
from handlers import *
from models import *

class Home(Handler):
    def get(self):
        self.render("home.html",
                    title="Teacher's Sched Maker")

class NewSY(Handler):
    def get(self):            
        self.render("new-sy.html",
                    title="Add new School Year")
        
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
                    title=self.sy.display())

class NewClass(Handler):
    def get(self):
        self.render("new-class.html", 
                    title=self.sy.display() + ' - New Class')

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
        self.render("class.html",
                    title=self.sy.display() + ' (Grade ' + str(self.myclass.level) + ' - ' + self.myclass.name + ')')

class NewTeacher(Handler):
    def get(self):
        self.render("new-teachers.html",
                    title=self.sy.display() + ' - New Teacher ')

    def post(self):
        sy = SY.get_by_id(int(self.request.get('id')))
        name = self.request.get("name")
        teacher = Teacher(name=name, parent=sy.key).put()
        self.next('teacher?id='+str(teacher.id())+'&parent='+str(sy.key.id()))

class viewTeacher(Handler):
    def get(self):
        self.render("teacher.html",
                    title=self.sy.display() + self.teacher.name)

class NewSubj(Handler):
    def get(self):
        self.render("new-subj.html",
                    title=self.sy.display() + ' - New Subject ')

    def post(self):
        sy = SY.get_by_id(int(self.request.get('id')))
        name = self.request.get("name")
        abrev = self.request.get("abrev")
        level = self.request.get("level")
        subject = Subject(name=name, abrev=abrev, level = int(level), parent=sy.key).put()
        self.next('subject?id='+str(subject.id())+'&parent='+str(sy.key.id()))

class viewSubj(Handler):
    def get(self):
        self.render("subj.html",
                    title= self.sy.display() + self.subject.abrev)


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/new-sy', NewSY),
    ('/sy', viewSY),
    ('/new-class', NewClass),
    ('/class', viewClass),
    ('/new-subject', NewSubj),
    ('/subject', viewSubj),
    ('/new-teacher', NewTeacher),
    ('/teacher', viewTeacher)
], debug=True)
