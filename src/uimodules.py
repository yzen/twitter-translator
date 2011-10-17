#! /usr/bin/env python

import tornado.web;

class Home(tornado.web.UIModule):
    def javascript_files(self):
        return ["js/home.js"]
        
    def css_files(self):
        return ["css/home.css"]

    def render(self):
        return self.render_string("html/uimodules/module-home.html")