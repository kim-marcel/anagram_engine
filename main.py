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
    def get(self):
        logging.error("GET")
        self.response.headers['Content-Type'] = 'text/html'

        # defining variables
        url = ''
        url_string = ''
        message = 'Welcome back. You have already logged in before.'

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
                message = 'Welcome to the application. This is your first login.'
                self.addNewUser(user)

        # if no user is logged in create login url
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        self.renderHTML(url, url_string, user, message,
                        self.getAnagramsOfUser(self.getMyUser()))

    # post method
    def post(self):
        logging.error("POST")
        self.response.headers['Content-Type'] = 'text/html'

        # get user data object from datastore of current user (logged in)
        myuser = self.getMyUser()

        text = self.request.get('anagram').lower()
        if text == None or text == '':
            pass
        else:
            # Add anagram to datastore
            anagramID = self.generateKey(text)
            anagramKey = ndb.Key('Anagrams', anagramID)
            anagrams = anagramKey.get()

            if anagrams:
                # an anagram with this key already exists
                myuser.addToAnagram(text, anagramKey)
            else:
                # this key doesnt exist --> write new anagram object to datastore
                myuser.addNewAnagram(text, myuser)

        # redirect to '/' --> MainPage
        self.redirect('/')

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

    def renderHTML(self, url, url_string, user, message, anagrams=None):
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'anagrams': anagrams,
            'message': message
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def getAnagramsOfUser(self, myUser):
        logging.error("Test")
        if myUser:
            logging.error("Logged in")
            logging.error(myUser.anagrams)
            myList = []

            for x in myUser.anagrams:
                anagrams = x.get()
                myList.append(anagrams)

            return myList

    def generateKey(self, text):
        key = text.lower()
        return ''.join(sorted(key))


# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
