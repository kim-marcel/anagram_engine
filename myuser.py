from google.appengine.ext import ndb
from anagrams import Anagrams


class MyUser(ndb.Model):
    # Object of anagrams where all the anagrams of the user are stored
    anagrams = ndb.KeyProperty(kind='Anagrams', repeated=True)

    def addNewAnagram(self, text):
        # instead of test the actual id should be used (alphabetically ordered text)
        key = self.generateKey(text)
        self.anagrams.append(ndb.Key('Anagrams', key))
        anagram = Anagrams(id=key)
        anagram.words.append(text)
        anagram.put()
        self.put()

    def addToAnagram(self, text, anagramKey):
        anagram = anagramKey.get()
        if text in anagram.words:
            # do nothing: word is already in there
            pass

        else:
            # append word
            anagram.words.append(text)
            # commit to datastore
            anagram.put()

    def generateKey(self, text):
        key = text.lower()
        return ''.join(sorted(key))
