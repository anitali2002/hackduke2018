from google.appengine.ext import ndb

class WordBank(ndb.Model):
    word = ndb.StringProperty(required = True)
    definition = ndb.StringProperty(required = True)
    disease = ndb.StringProperty(required = False)
