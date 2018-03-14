from google.appengine.ext import ndb
from anagrams import Anagrams


class MyUser(ndb.Model):
    # Object of anagrams where all the anagrams of the user are stored
    anagrams = ndb.KeyProperty(kind='Anagrams', repeated=True)

    def addNewAnagram(self, text, myUser):
        # instead of test the actual id should be used (alphabetically ordered text)
        key = self.generateKey(text)
        myUser.anagrams.append(ndb.Key('Anagrams', key))
        anagram = Anagrams(id=key)
        anagram.words.append(text)
        anagram.put()
        myUser.put()
        # self.anagrams.append(anagram)

        # commit to datastore
        # self.put()

    def addToAnagram(self, text, anagramKey):
        # instead of test the actual id should be used (alphabetically ordered text)
        key = self.generateKey(text)
        anagram = anagramKey.get()
        anagram.words.append(text)
        # self.anagrams.append(anagram)

        # commit to datastore
        anagram.put()

    def generateKey(self, text):
        key = text.lower()
        return ''.join(sorted(key))
