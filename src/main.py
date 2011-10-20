#! /usr/bin/env python

import os
import urlparse
import urllib
import tornado.ioloop
import tornado.web
import tornado.locale
import tornado.httpclient
import tornado.escape
import uimodules

class AppRequestHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        #TODO: TEST
        self.lang = self.locale.code[0:2]
    #TODO: Test
    def buildRequestUrl(self, urlBase, **params):
        return urlBase + "?" + urllib.urlencode(params)

class HomeHandler(AppRequestHandler):
    def get(self):
        self.render("html/home.html", tweets=[], lang=self.lang, query="")

class SearchHandler(AppRequestHandler):
    def get(self):
        self.redirect("/")

    @tornado.web.asynchronous
    def post(self):
        query = urlparse.parse_qs(self.request.body)
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(self.buildRequestUrl("http://search.twitter.com/search.json", q=query["query"][0]), callback=self.on_search)

    def on_search(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        data = tornado.escape.json_decode(response.body)
        self.render("html/home.html", tweets=data["results"], lang=self.lang, query=data["query"])
        
class TranslateHandler(AppRequestHandler):
    @tornado.web.asynchronous
    def post(self):
        query = urlparse.parse_qs(self.request.body)
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(self.buildRequestUrl("https://ajax.googleapis.com/ajax/services/language/translate", v="1.0", q=query["text"][0], langpair=query["lang"][0] + "|" + self.lang), callback=self.on_translate, headers={"Referer": self.request.headers["Referer"]})
        
    def on_translate(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        data = tornado.escape.json_decode(response.body)
        self.write(data["responseData"])
        self.finish()

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "ui_modules": uimodules
}

application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/search", SearchHandler),
    (r"/translate", TranslateHandler)
], **settings)

if __name__ == "__main__":
    tornado.locale.load_translations(os.path.join(os.path.dirname(__file__), "translations"))
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()