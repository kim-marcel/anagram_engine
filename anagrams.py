from google.appengine.ext import ndb


class Anagrams(ndb.Model):
    # List with all the anagrams for given set of chars
    words = ndb.StringProperty(repeated=True)
