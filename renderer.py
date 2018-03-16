import jinja2
import os
import utilities

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


def renderMainHTML(self, url, url_string, anagrams):
    template_values = {
        'url': url,
        'url_string': url_string,
        'user': utilities.getUser(),
        'anagrams': anagrams,
    }

    template = JINJA_ENVIRONMENT.get_template('main.html')
    self.response.write(template.render(template_values))


def renderSearchHTML(self, numberSearch, searchResult):
    template_search_values = {
        'isNumberSearch': numberSearch,
        'searchResult': searchResult,
    }

    template = JINJA_ENVIRONMENT.get_template('searchResult.html')
    self.response.write(template.render(template_search_values))
