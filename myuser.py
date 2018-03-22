from google.appengine.ext import ndb
from anagrams import Anagrams


class MyUser(ndb.Model):
    # Object of anagrams where all the anagrams of the user are stored
    anagrams = ndb.KeyProperty(kind='Anagrams', repeated=True)
