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

from tornado.options import define, options
"""Define web application options"""
define("port", default=8888)
define("twitterUrl")
define("googleTranslateUrl")

#TODO: TEST
"""Build an absolute path to a resource."""
def getAbsolutePath(relPath):
    return os.path.join(os.path.dirname(__file__), relPath)

"""
    tornado.web.Application subclass that implements it with defined settings and 
    handlers.
"""
class WebApplication(tornado.web.Application):
    def __init__(self):
        """Web application's settings."""
        settings = {
            "static_path": getAbsolutePath("static"),
            "ui_modules": uimodules
        }
        tornado.web.Application.__init__(self, [
            (r"/", HomeHandler),
            (r"/search", SearchHandler),
            (r"/translate", TranslateHandler)
        ], **settings)

"""
    tornado.web.RequestHandler's subclass that helps to abstract some of the handler's
    asynchronous functionality.
"""
class AppRequestHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        #TODO: TEST
        """lang field contains a short version of current user's locale."""
        self.lang = self.locale.code[0:2]
    #TODO: Test
    """
        A helper method that builds a full url out of an url base and parameters
        delivered as keyword arguments.
    """
    def buildRequestUrl(self, urlBase, **params):
        return urlBase + "?" + urllib.urlencode(params)

    #TODO: Test
    """
        A callback that's executed after http.fetch when an asynchronous request
        handler is complete.
    """
    def handleRequestCallback(self, data):
        """Override in subclass - a handle request callback when making async requests."""
        return None

    #TODO: Test
    """
        handlerRequestCallback's wrapper that checks for reponse error and parses json 
        body.
    """
    def on_resonse(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        data = tornado.escape.json_decode(response.body)
        self.handleRequestCallback(data)
"""
    AppRequestHandler's subclass that handles GET requests to '/' url.
"""
class HomeHandler(AppRequestHandler):
    def get(self):
        self.render("html/home.html", tweets=[], lang=self.lang, query="")

"""
    AppRequestHandler's subclass that handles GET and POST requests to '/search' url.
"""
class SearchHandler(AppRequestHandler):
    """Redirect to base url if the user tries to GET to /search."""
    def get(self):
        self.redirect("/")

    """Handle POST request to '/search' and search twitter for that query string."""
    @tornado.web.asynchronous
    def post(self):
        query = urlparse.parse_qs(self.request.body)
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(self.buildRequestUrl(options.twitterUrl,
            q=query["query"][0]),
            callback=self.on_resonse)

    """Overridden handleRequestCallback that renders twitter search results."""
    def handleRequestCallback(self, data):
        self.render("html/home.html", tweets=data["results"], lang=self.lang, query=data["query"])

"""
    AppRequestHandler's subclass that handles GET requests to '/translate' url.
"""
class TranslateHandler(AppRequestHandler):
    """Handle GET request to '/translate' and google translate the selected tweet."""
    @tornado.web.asynchronous
    def get(self):
        query = self.request.arguments
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(self.buildRequestUrl(options.googleTranslateUrl,
            v="1.0", q=query["text"][0], langpair=query["lang"][0] + "|" + self.lang),
            callback=self.on_resonse,
            headers={"Referer": self.request.headers["Referer"]})

    """
        Overridden handleRequestCallback that writes google translate response as 
        its own response data.
    """
    def handleRequestCallback(self, data):
        self.write(data["responseData"])
        self.finish()

def main():
    """Load translations"""
    tornado.locale.load_translations(getAbsolutePath("translations"))
    """Load web app config stored at src/app.conf"""
    tornado.options.parse_config_file(getAbsolutePath("app.conf"))
    application = WebApplication()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()