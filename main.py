import webapp2
import jinja2
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from anagrams import Anagrams

# import MyUser class from myuser.py
from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    # GET method
    def get(self):
        logging.debug("GET")
        self.response.headers['Content-Type'] = 'text/html'

        # defining variables
        url = ''
        url_string = ''

        # get current user (returns none if no user is logged in)
        user = self.getUser()

        # check whether user is logged in
        if self.isLoggedIn():
            # generate logout url
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser = self.getMyUser()

            # if myuser object is None --> No user with key found --> new user --> make new user in datastore
            if myuser == None:
                self.addNewUser(user)

        # if no user is logged in create login url
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        self.renderMainHTML(url, url_string, user,
                            self.getAnagramsOfUser(self.getMyUser()))

    # POST method
    def post(self):
        logging.debug("POST")
        self.response.headers['Content-Type'] = 'text/html'

        # get user data object from datastore of current user (logged in)
        myuser = self.getMyUser()
        button = self.request.get('button')
        inputText = self.request.get('anagram').lower()

        if button == 'Add':
            self.add(myuser, inputText)
            # redirect to '/' --> MainPage
            self.redirect('/')

        elif button == 'Search':
            searchResult = self.search(inputText, myuser)
            self.renderSearchHTML(searchResult)

        elif button == 'Show':
            number = self.request.get('number')
            if number:
                number = int(number)
                if number > 0:
                    logging.debug('Search for anagrams with ' +
                                  str(number) + ' letters.')
            self.redirect('/')

    def add(self, myuser, text):
        logging.debug('Add something')
        if text == None or text == '':
            pass

        else:
            # Add anagram to datastore
            anagramID = myuser.key.id() + '/' + Anagrams.generateKey(text)
            anagramKey = ndb.Key('Anagrams', anagramID)
            anagrams = anagramKey.get()

            if anagrams:
                # an anagram with this key already exists
                myuser.addToAnagram(text, anagramKey)
            else:
                # this key doesnt exist --> write new anagram object to datastore
                myuser.addNewAnagram(text)

    # returns a list with all the items (if nothing found returns None)
    def search(self, text, myuser):
        logging.debug('Search: ' + text)
        anagramID = myuser.key.id() + '/' + Anagrams.generateKey(text)
        anagrams = self.getAnagramsOfUser(myuser)
        result = None
        for anagram in anagrams:
            logging.debug(anagram.key.id())
            if anagram.key.id() == anagramID:
                for word in anagram.words:
                    if word == text:
                        logging.debug('Success!!!')
                        result = anagram.words
                        result.remove(text)
                        logging.debug(result)
                        break
        return result

    # get user from data
    def getMyUser(self):
        user = self.getUser()
        if user:
            myuser_key = ndb.Key('MyUser', user.user_id())
            return myuser_key.get()

    # Get user from this page
    def getUser(self):
        return users.get_current_user()

    def isLoggedIn(self):
        # get current user (returns none if no user is logged in)
        user = self.getUser()
        if(user):
            return True
        else:
            return False

    def addNewUser(self, user):
        myuser = MyUser(id=user.user_id())
        # commit to datastore
        myuser.put()

    def renderMainHTML(self, url, url_string, user, anagrams):
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'anagrams': anagrams,
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def renderSearchHTML(self, searchResult):
        template_search_values = {
            'searchResult': searchResult
        }

        template = JINJA_ENVIRONMENT.get_template('searchResult.html')
        self.response.write(template.render(template_search_values))

    def getAnagramsOfUser(self, myUser):
        logging.debug("Test")
        if myUser:
            logging.debug("Logged in")
            logging.debug(myUser.anagrams)
            myList = []

            for x in myUser.anagrams:
                anagrams = x.get()
                myList.append(anagrams)

            return myList


# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
