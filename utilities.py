from google.appengine.ext import ndb
from google.appengine.api import users
from myuser import MyUser
from anagrams import Anagrams
import logging

# Get user from this page


def getUser():
    return users.get_current_user()

# get user from data


def getMyUser():
    user = getUser()
    if user:
        myuser_key = ndb.Key('MyUser', user.user_id())
        return myuser_key.get()


def isLoggedIn():
    # get current user (returns none if no user is logged in)
    user = getUser()
    if(user):
        return True
    else:
        return False


def addNewUser(user):
    myuser = MyUser(id=user.user_id())
    # commit to datastore
    myuser.put()


def getAnagramsOfUser(myUser):
    if myUser:
        logging.debug("Logged in")
        logging.debug(myUser.anagrams)
        myList = []

        for x in myUser.anagrams:
            anagrams = x.get()
            myList.append(anagrams)

        return myList


def addNewAnagram(myuser, text):
    generatedKey = Anagrams.generateKey(text)
    key = myuser.key.id() + '/' + generatedKey
    myuser.anagrams.append(ndb.Key('Anagrams', key))
    myuser.put()
    anagram = Anagrams(id=key)
    anagram.words.append(text)
    anagram.sortedWord = generatedKey
    anagram.put()


def addToAnagram(text, anagramKey):
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

# returns true if the number is valid (positive and not None)


def numberIsValid(number):
    if number:
        number = int(number)
        if number > 0:
            return True
    return False


def getLoginURL(mainPage):
    return users.create_login_url(mainPage.request.uri)


def getLogoutURL(mainPage):
    return users.create_logout_url(mainPage.request.uri)
