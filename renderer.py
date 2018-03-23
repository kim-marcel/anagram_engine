import jinja2
import os
import utilities

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def renderLoginHTML(self, url):
    template_values = {'url': url}

    template = JINJA_ENVIRONMENT.get_template('/templates/login.html')
    self.response.write(template.render(template_values))


def renderMainHTML(self, url, anagrams):
    template_values = {
        'url': url,
        'user': utilities.getUser(),
        'anagrams': anagrams,
    }

    template = JINJA_ENVIRONMENT.get_template('/templates/main.html')
    self.response.write(template.render(template_values))


def renderSearchHTML(self, numberSearch, searchTerm, searchResult):
    template_search_values = {
        'isNumberSearch': numberSearch,
        'searchTerm': searchTerm,
        'searchResult': searchResult,
    }

    template = JINJA_ENVIRONMENT.get_template('/templates/searchResult.html')
    self.response.write(template.render(template_search_values))
