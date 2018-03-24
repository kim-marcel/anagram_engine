import jinja2
import os
import utilities

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def render_login(self, url):
    template_values = {'url': url}

    template = JINJA_ENVIRONMENT.get_template('/templates/login.html')
    self.response.write(template.render(template_values))


def render_main(self, url, anagrams):
    template_values = {
        'url': url,
        'user': utilities.get_user(),
        'anagrams': anagrams,
    }

    template = JINJA_ENVIRONMENT.get_template('/templates/main.html')
    self.response.write(template.render(template_values))


def render_search(self, is_number_search, search_term, search_result):
    template_search_values = {
        'is_number_search': is_number_search,
        'search_term': search_term,
        'search_result': search_result,
    }

    template = JINJA_ENVIRONMENT.get_template('/templates/searchResult.html')

    self.response.write(template.render(template_search_values))
