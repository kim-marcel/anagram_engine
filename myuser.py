import logging
from google.appengine.ext import ndb
from anagrams import Anagrams


class MyUser(ndb.Model):
    # Object of anagrams where all the anagrams of the user are stored
    anagrams = ndb.KeyProperty(kind='Anagrams', repeated=True)

    def addNewAnagram(self, text):
        generatedKey = Anagrams.generateKey(text)
        key = self.key.id() + '/' + generatedKey
        self.anagrams.append(ndb.Key('Anagrams', key))
        anagram = Anagrams(id=key)
        anagram.words.append(text)
        anagram.sortedWord = generatedKey
        anagram.put()
        self.put()

    def addToAnagram(self, text, anagramKey):
        anagram = anagramKey.get()
        if text in anagram.words:
            # do nothing: word is already in there
            logging.debug(text + ' already exists.')
            pass

        else:
            # append word
            anagram.words.append(text)
            # commit to datastore
            anagram.put()
