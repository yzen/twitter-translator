#! /usr/bin/env python

import tornado.web;

class Home(tornado.web.UIModule):
    def javascript_files(self):
        return ["js/home.js"]
        
    def css_files(self):
        return ["css/home.css"]

    def render(self, tweets, locale):
        return self.render_string("html/uimodules/module-home.html", tweets=tweets, locale=locale)

class Tweet(tornado.web.UIModule):
    def render(self, tweet):
        return self.render_string("html/uimodules/module-tweet.html", tweet=tweet)