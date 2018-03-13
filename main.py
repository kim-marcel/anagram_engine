import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

# import MyUser class from myuser.py
from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # defining variables
        url = ''
        url_string = ''
        welcome = 'Welcome back'

        # get current user (returns none if no user is logged in)
        user = users.get_current_user()

        # check whether user is logged in
        if user:
            # generate logout url
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            # generate key object to find Object of type MyUser with user-id from datastore
            myuser_key = ndb.Key('MyUser', user.user_id())
            # get user object with key object
            myuser = myuser_key.get()

            # if myuser object is None --> No user with key found --> new user --> make new user in datastore
            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id())
                # commit to datastore
                myuser.put()

        # if no user is logged in create login url
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'welcome': welcome
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
