#! /usr/bin/env python

import tornado.web;

class Home(tornado.web.UIModule):
    def javascript_files(self):
        return ["lib/jquery-1.6.4.min.js", "js/home.js"]
        
    def css_files(self):
        return ["css/home.css"]

    def render(self, tweets, lang, query):
        return self.render_string("html/uimodules/module-home.html", tweets=tweets, lang=lang, query=query)

class Tweet(tornado.web.UIModule):
    def render(self, tweet, lang):
        return self.render_string("html/uimodules/module-tweet.html", tweet=tweet, lang=lang)

class Translate(tornado.web.UIModule):
    def render(self):
        return self.render_string("html/uimodules/module-translate.html")