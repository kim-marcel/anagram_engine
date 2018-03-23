from google.appengine.ext import ndb
import webapp2
import logging
import renderer
import utilities
from anagrams import Anagrams


class MainPage(webapp2.RequestHandler):
    # GET-request
    def get(self):
        logging.debug("GET")
        self.response.headers['Content-Type'] = 'text/html'

        # check whether user is logged in
        if utilities.userIsLoggedIn():
            # if myuser object is None --> No user with key found --> new user --> make new user in datastore
            if not utilities.userExists():
                utilities.addNewUser(utilities.getUser())

            renderer.renderMainHTML(self, utilities.getLogoutURL(self),
                                    utilities.getAnagramsOfUser(
                                        utilities.getMyUser()))

        # if no user is logged in create login url
        else:
            renderer.renderLoginHTML(self, utilities.getLoginURL(self))

    # POST-request
    def post(self):
        logging.debug("POST")
        self.response.headers['Content-Type'] = 'text/html'

        # get user data object from datastore of current user (logged in)
        myuser = utilities.getMyUser()
        button = self.request.get('button')
        inputText = utilities.prepareTextInput(self.request.get('value'))
        logging.debug(inputText)
        logging.debug(button)

        if button == 'Add':
            self.add(inputText, myuser)
            self.redirect('/')

        elif button == 'Search':
            searchResult = self.search(inputText, myuser)
            renderer.renderSearchHTML(self, False, inputText, searchResult)

        elif button == 'Show':
            number = self.request.get('number')
            if utilities.numberIsValid(number):
                result = self.numberSearch(number, myuser)
                renderer.renderSearchHTML(self, True, number, result)
            else:
                self.redirect('/')

        elif button == 'Delete':
            anagramId = myuser.key.id() + '/' + str(
                self.request.get('anagram_id'))
            self.delete(myuser, anagramId)
            self.redirect('/')

        elif button == 'Generate':
            words = self.generate(inputText)
            renderer.renderSearchHTML(self, False, inputText, words)

    def add(self, text, myuser):
        logging.debug('Add ' + text)
        if text == None or text == '':
            pass

        else:
            # Add anagram to datastore
            anagramID = myuser.key.id() + '/' + utilities.generateId(text)
            anagramKey = ndb.Key('Anagrams', anagramID)
            anagrams = anagramKey.get()

            if anagrams:
                # an anagram with this key already exists
                utilities.addToAnagram(text, anagramKey)
            else:
                # this key doesnt exist --> write new anagram object to datastore
                utilities.addNewAnagram(myuser, text)

    # returns a list with all the items (if nothing found returns None)
    def search(self, text, myuser):
        logging.debug('Search: ' + text)
        anagramID = myuser.key.id() + '/' + utilities.generateId(text)
        anagram = ndb.Key('Anagrams', anagramID).get()

        if anagram:
            result = anagram.words
            result.remove(text)
            return result
        else:
            return None

    def numberSearch(self, number, myuser):
        number = int(number)
        result = Anagrams.query(Anagrams.length == number, Anagrams.userId == myuser.key.id()).fetch()
        return result

    def delete(self, myuser, anagramId):
        myuser.anagrams.remove(ndb.Key('Anagrams', anagramId))
        myuser.put()
        ndb.Key('Anagrams', anagramId).delete()

    def generate(self, inputText):
        permutations = utilities.allPermutations(inputText)
        words = utilities.filterEnglishWords(permutations)
        if inputText in words:
            words.remove(inputText)
        return words


# starts the web application and specifies the routing table
app = webapp2.WSGIApplication(
    [
        ('/', MainPage),
    ], debug=True)
