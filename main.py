import webapp2
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from anagrams import Anagrams
import renderer
import utilities


class MainPage(webapp2.RequestHandler):
    # GET method
    def get(self):
        logging.debug("GET")
        self.response.headers['Content-Type'] = 'text/html'

        # defining variables
        url = ''
        url_string = ''

        # check whether user is logged in
        if utilities.isLoggedIn():
            # generate logout url
            url = utilities.getLogoutURL(self)
            url_string = 'logout'

            myuser = utilities.getMyUser()

            # if myuser object is None --> No user with key found --> new user --> make new user in datastore
            if myuser == None:
                utilities.addNewUser(utilities.getUser())

        # if no user is logged in create login url
        else:
            url = utilities.getLoginURL(self)
            url_string = 'login'

        renderer.renderMainHTML(self, url, url_string,
                                utilities.getAnagramsOfUser(utilities.getMyUser()))

    # POST method
    def post(self):
        logging.debug("POST")
        self.response.headers['Content-Type'] = 'text/html'

        # get user data object from datastore of current user (logged in)
        myuser = utilities.getMyUser()
        button = self.request.get('button')
        inputText = self.request.get('anagram').lower()

        if button == 'Add':
            self.add(inputText, myuser)
            # redirect to '/' --> MainPage
            self.redirect('/')

        elif button == 'Search':
            searchResult = self.search(inputText, myuser)
            renderer.renderSearchHTML(self, False, searchResult)

        elif button == 'Show':
            number = self.request.get('number')
            if utilities.numberIsValid(number):
                result = self.numberSearch(number, myuser)
                renderer.renderSearchHTML(self, True, result)
            else:
                self.redirect('/')

    def add(self, text, myuser):
        logging.debug('Add ' + text)
        if text == None or text == '':
            pass

        else:
            # Add anagram to datastore
            anagramID = myuser.key.id() + '/' + Anagrams.generateKey(text)
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
        anagramID = myuser.key.id() + '/' + Anagrams.generateKey(text)
        anagrams = utilities.getAnagramsOfUser(myuser)
        result = None
        for anagram in anagrams:
            logging.debug(anagram.key.id())
            if anagram.key.id() == anagramID:
                for word in anagram.words:
                    if word == text:
                        result = anagram.words
                        result.remove(text)
                        break
        return result

    def numberSearch(self, number, myuser):
        result = []
        number = int(number)
        anagrams = utilities.getAnagramsOfUser(myuser)
        for anagram in anagrams:
            if len(anagram.sortedWord) == number:
                result.append(anagram)
        return result


# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
