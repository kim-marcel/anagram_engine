from google.appengine.ext import ndb


class Anagrams(ndb.Model):
    # alphabetically sorted word
    sortedWord = ndb.StringProperty()
    # List with all the anagrams for given set of chars
    words = ndb.StringProperty(repeated=True)

    @staticmethod
    def generateKey(text):
        key = text.lower()
        return ''.join(sorted(key))
