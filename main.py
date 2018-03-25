from google.appengine.ext import ndb
import webapp2
import logging
import renderer
import utilities
from anagram import Anagram


class MainPage(webapp2.RequestHandler):
    # GET-request
    def get(self):
        logging.debug("GET")
        self.response.headers['Content-Type'] = 'text/html'

        # check whether user is logged in
        if utilities.user_is_logged_in():
            # if myuser object is None --> No user with key found --> new user --> make new user in datastore
            if not utilities.user_exists():
                utilities.add_new_user(utilities.get_user())

            renderer.render_main(self, utilities.get_logout_url(self),
                                 utilities.get_anagrams_of_user(utilities.get_my_user()))

        # if no user is logged in create login url
        else:
            renderer.render_login(self, utilities.get_login_url(self))

    # POST-request
    def post(self):
        logging.debug("POST")
        self.response.headers['Content-Type'] = 'text/html'

        # get user data object from datastore of current user (logged in)
        my_user = utilities.get_my_user()
        button = self.request.get('button')
        input_text = utilities.prepare_text_input(self.request.get('value'))
        logging.debug(input_text)
        logging.debug(button)

        if button == 'Add':
            self.add(input_text, my_user)
            self.redirect('/')

        elif button == 'Search':
            search_result = self.search(input_text, my_user)
            renderer.render_search(self, False, input_text, search_result)

        elif button == 'Show':
            number = self.request.get('number')
            if utilities.number_is_valid(number):
                result = self.number_search(number, my_user)
                renderer.render_search(self, True, number, result)
            else:
                self.redirect('/')

        elif button == 'Delete':
            anagram_id = my_user.key.id() + '/' + str(self.request.get('anagram_id'))
            self.delete(my_user, anagram_id)
            self.redirect('/')

        elif button == 'Generate':
            words = self.generate(input_text)
            renderer.render_search(self, False, input_text, words)

    def add(self, text, my_user):
        logging.debug('Add ' + text)
        if text is not None or text != '':
            # Add anagram to datastore
            anagram_id = my_user.key.id() + '/' + utilities.generate_id(text)
            anagram_key = ndb.Key(Anagram, anagram_id)
            anagrams = anagram_key.get()

            if anagrams:
                # an anagram with this key already exists
                utilities.add_to_anagram(text, anagram_key)
            else:
                # this key doesnt exist --> write new anagram object to datastore
                utilities.add_new_anagram(my_user, text, anagram_id, anagram_key)

    # returns a list with all the items (if nothing found returns None)
    def search(self, text, my_user):
        logging.debug('Search: ' + text)
        anagram_id = my_user.key.id() + '/' + utilities.generate_id(text)
        anagram = ndb.Key(Anagram, anagram_id).get()

        if anagram:
            result = anagram.words
            result.remove(text)
            return result
        else:
            return None

    def number_search(self, number, my_user):
        number = int(number)
        result = Anagram.query(Anagram.length == number, Anagram.user_id == my_user.key.id()).fetch()
        return result

    def delete(self, my_user, anagram_id):
        anagram_key = ndb.Key(Anagram, anagram_id)
        if anagram_key in my_user.anagrams:
            my_user.anagrams.remove(anagram_key)
            my_user.put()
            ndb.Key(Anagram, anagram_id).delete()

    def generate(self, input_text):
        permutations = utilities.all_permutations(input_text)
        words = utilities.filter_english_words(permutations)
        if input_text in words:
            words.remove(input_text)
        return words


# starts the web application and specifies the routing table
app = webapp2.WSGIApplication(
    [
        ('/', MainPage),
    ], debug=True)
