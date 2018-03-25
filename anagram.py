from google.appengine.ext import ndb


class Anagram(ndb.Model):
    # alphabetically sorted word
    sorted_word = ndb.StringProperty()
    # length of the anagram
    length = ndb.IntegerProperty()
    # The id of the user to whom this anagram belongs
    user_id = ndb.StringProperty()
    # List with all the anagrams for given set of chars
    words = ndb.StringProperty(repeated=True)
