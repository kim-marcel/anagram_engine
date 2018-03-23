from google.appengine.ext import ndb


class Anagrams(ndb.Model):
    # alphabetically sorted word
    sortedWord = ndb.StringProperty()
    # length of the anagram
    length = ndb.IntegerProperty()
    # The id of the user to whom this anagram belongs
    userId = ndb.StringProperty()
    # List with all the anagrams for given set of chars
    words = ndb.StringProperty(repeated=True)
