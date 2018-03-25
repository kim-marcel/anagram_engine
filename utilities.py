from google.appengine.ext import ndb
from google.appengine.api import users
from myuser import MyUser
from anagram import Anagram
import logging
import re  # regex

# define global variable as a list with all english words read from a file
with open("wordsEn.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)


# Get user from this page
def get_user():
    return users.get_current_user()


# get user from data
def get_my_user():
    user = get_user()
    if user:
        my_user_key = ndb.Key(MyUser, user.user_id())
        return my_user_key.get()


def user_is_logged_in():
    return True if get_user() else False


# returns true if for this user a myuser object already exists in the datastore
def user_exists():
    return True if get_my_user() else False


def add_new_user(user):
    MyUser(id=user.user_id()).put()


def get_anagrams_of_user(my_user):
    if my_user:
        logging.debug(my_user.anagrams)
        result = []

        for anagram in my_user.anagrams:
            anagrams = anagram.get()
            result.append(anagrams)

        return result


def add_new_anagram(my_user, text, anagram_id, anagram_key):
    if is_english_word(text):
        anagram = Anagram(id=anagram_id)
        anagram.words.append(text)
        anagram.sorted_word = generate_id(text)
        anagram.length = len(text)
        anagram.user_id = my_user.key.id()
        anagram.put()
        # add key of the new anagram to the users KeyProperty
        my_user.anagrams.append(anagram_key)
        my_user.put()


def add_to_anagram(text, anagram_key):
    anagram = anagram_key.get()
    if text not in anagram.words:
        if is_english_word(text):
            # append word
            anagram.words.append(text)
            # commit to datastore
            anagram.put()


def generate_id(text):
    key = text.lower()
    return ''.join(sorted(key))


# return a list of all permutations of a given string
def all_permutations(input_string):
    if len(input_string) == 1:
        return input_string

    result = []
    for letter in input_string:
        for perm in all_permutations(input_string.replace(letter, '', 1)):
            result.append(letter + perm)

    return result


# returns true if the given string is an english word
def is_english_word(text):
    return True if text in english_words else False


# get a list with words and filter this list
# returns a list with only the english words
def filter_english_words(word_list):
    result = []
    for word in word_list:
        if word in english_words:
            if word not in result:
                result.append(word)

    return result


# returns true if the number is valid (positive and not None)
def number_is_valid(number):
    if number:
        number = int(number)
        if number > 0:
            return True
    return False


def prepare_text_input(input_text):
    result = input_text.lower()
    result = re.sub('[^a-z]+', '', result)
    return result


def get_login_url(main_page):
    return users.create_login_url(main_page.request.uri)


def get_logout_url(main_page):
    return users.create_logout_url(main_page.request.uri)
