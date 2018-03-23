from google.appengine.ext import ndb
from google.appengine.api import users
from myuser import MyUser
from anagrams import Anagrams
import logging
import re  #regex

# define global variable as a list with all english words read from a file
with open("wordsEn.txt") as wordFile:
    englishWords = set(word.strip().lower() for word in wordFile)


# Get user from this page
def getUser():
    return users.get_current_user()


# get user from data
def getMyUser():
    user = getUser()
    if user:
        myuser_key = ndb.Key('MyUser', user.user_id())
        return myuser_key.get()


def userIsLoggedIn():
    return True if getUser() else False


# returns true if for this user a myuser object already exists in the datastore
def userExists():
    return True if getMyUser() else False


def addNewUser(user):
    MyUser(id=user.user_id()).put()


def getAnagramsOfUser(myUser):
    if myUser:
        logging.debug(myUser.anagrams)
        result = []

        for anagram in myUser.anagrams:
            anagrams = anagram.get()
            result.append(anagrams)

        return result


def addNewAnagram(myuser, text):
    if isEnglishWord(text):
        generatedKey = generateId(text)
        key = myuser.key.id() + '/' + generatedKey
        anagram = Anagrams(id=key)
        anagram.words.append(text)
        anagram.sortedWord = generatedKey
        anagram.length = len(text)
        anagram.userId = myuser.key.id()
        anagram.put()
        # add key of the new anagram to the users KeyProperty
        myuser.anagrams.append(ndb.Key('Anagrams', key))
        myuser.put()


def addToAnagram(text, anagramKey):
    anagram = anagramKey.get()
    if text not in anagram.words:
        if isEnglishWord(text):
            # append word
            anagram.words.append(text)
            # commit to datastore
            anagram.put()


def generateId(text):
    key = text.lower()
    return ''.join(sorted(key))


# return a list of all permutations of a given string
def allPermutations(inputString):
    if len(inputString) == 1:
        return inputString

    result = []
    for letter in inputString:
        for perm in allPermutations(inputString.replace(letter, '', 1)):
            result.append(letter + perm)

    return result


# returns true if the given string is an english word
def isEnglishWord(text):
    return True if text in englishWords else False


# get a list with words and filter this list
# returns a list with only the english words
def filterEnglishWords(wordList):
    result = []
    for word in wordList:
        if word in englishWords:
            if word not in result:
                result.append(word)

    return result


# returns true if the number is valid (positive and not None)
def numberIsValid(number):
    if number:
        number = int(number)
        if number > 0:
            return True
    return False


def prepareTextInput(inputText):
    result = inputText.lower()
    result = re.sub('[^a-z]+', '', result)
    return result


def getLoginURL(mainPage):
    return users.create_login_url(mainPage.request.uri)


def getLogoutURL(mainPage):
    return users.create_logout_url(mainPage.request.uri)
