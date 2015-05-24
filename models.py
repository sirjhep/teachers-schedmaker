from google.appengine.ext import ndb

class Sched(ndb.Model):
    """ Except for `day` and `level`, everything should be the Id of that specific ndb Model."""
    
    # Name of the teacher who will teach
    teacher = ndb.IntegerProperty()
    
    # Subject to teach (Subject Key)
    subject = ndb.IntegerProperty()
    
    # To what level
    level = ndb.IntegerProperty()
    
    # To what section
    section = ndb.IntegerProperty()
    
    # The time of the day the subject will be taught
    # This cannot be changed once created
    timeod = ndb.IntegerProperty(required=True)
    
    # The day when the subject will be taught.
    # This cannot be changed once created
    day = ndb.StringProperty(required=True)


class Teacher(ndb.Model):
    """ All info about a teacher """
    
    # Name, in any format.
    name = ndb.StringProperty()
    
    # Id of Subjects being taught
    scheds = ndb.IntegerProperty(repeated=True)

    # Subjects taught
    subjects = ndb.IntegerProperty(repeated=True)


class Subject(ndb.Model):
    """ Subjects are always associated with level """
    name = ndb.StringProperty(required=True)
    abrev = ndb.StringProperty(required=True) #Example: SCI
    level = ndb.IntegerProperty(required=True)

class Section(ndb.Model):
    name = ndb.StringProperty(required=True)
    level = ndb.IntegerProperty(required=True)
    adviser = ndb.IntegerProperty() # key of Teacher

class TimeOD(ndb.Model):
    start = ndb.StringProperty(required=True)
    recess = ndb.StringProperty(default=False)
    seq_number = ndb.IntegerProperty()