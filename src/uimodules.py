#! /usr/bin/env python

import tornado.web;

class Home(tornado.web.UIModule):
    def javascript_files(self):
        return ["lib/jquery-1.6.4.min.js", "js/home.js"]
        
    def css_files(self):
        return ["css/home.css"]

    def render(self, tweets, locale, query):
        return self.render_string("html/uimodules/module-home.html", tweets=tweets, locale=locale, query=query)

class Tweet(tornado.web.UIModule):
    def render(self, tweet):
        return self.render_string("html/uimodules/module-tweet.html", tweet=tweet)