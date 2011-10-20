#! /usr/bin/env python

import tornado.web;

""" Home UIModule that is the base template module for all pages ('/' and '/search')."""
class Home(tornado.web.UIModule):

    """Load js files."""
    def javascript_files(self):
        return ["lib/jquery-1.6.4.min.js", "js/home.js"]

    """Load css files."""
    def css_files(self):
        return ["css/home.css"]

    """
        Render Home module using module-home.html template and appropriate data passed as
        keyword arguments (list of tweets, current user's language and search query string).
    """
    def render(self, tweets, lang, query):
        return self.render_string("html/uimodules/module-home.html", tweets=tweets, lang=lang, query=query)

""" Tweet UIModule that is the template module for rendering tweet entities."""
class Tweet(tornado.web.UIModule):
    """
        Render Tweet module using module-tweet.html template and appropriate data passed as
        keyword arguments (tweet information and current user's language).
    """
    def render(self, tweet, lang):
        return self.render_string("html/uimodules/module-tweet.html", tweet=tweet, lang=lang)

"""
    Translate UIModule that is the template module for conditional rendering of every
    tweet's translate button.
"""
class Translate(tornado.web.UIModule):
    """
        Render Translate (button) module using module-translate.html template.
    """
    def render(self):
        return self.render_string("html/uimodules/module-translate.html")