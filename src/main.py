#! /usr/bin/env python

import os
import cgi
import tornado.ioloop
import tornado.web
import tornado.locale
import uimodules

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html/home.html", tweets=[], locale=self.locale.code)

class SearchHandler(tornado.web.RequestHandler):
    def post(self):
        query = cgi.parse_qs(self.request.body)
        self.render("html/home.html", tweets=[], locale=self.locale.code)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "ui_modules": uimodules
}

application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/search", SearchHandler)
], **settings)

if __name__ == "__main__":
    tornado.locale.load_translations(os.path.join(os.path.dirname(__file__), "translations"))
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()