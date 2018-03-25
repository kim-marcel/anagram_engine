from google.appengine.ext import ndb
from anagram import Anagram


class MyUser(ndb.Model):
    # Object of anagrams where all the anagrams of the user are stored
    anagrams = ndb.KeyProperty(kind=Anagram, repeated=True)
