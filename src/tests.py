#! /usr/bin/env python

import unittest
import os
import tornado.testing
import tornado.httpserver
import tornado.web
from main import *
from HTMLParser import HTMLParser

class responseHTMLParser(HTMLParser):
    def __init__(self, callback):
        self.callback = callback
        HTMLParser.__init__(self)
    
    """If parser find <p> tag that corresponds to a tweet call a callback."""
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "p": self.callback()

"""Integration Tests for WebApplication class from main.py"""
class WebApplicationTest(tornado.testing.AsyncHTTPTestCase):
    """Success response code to compare to."""
    _successCode = 200

    def get_app(self):
        return WebApplication()
        
    def homeParserCallback(self):
        self.fail("There should be no tweets")
        
    def defaultHandler(self, url):
        self.http_client.fetch(self.get_url(url), self.stop)
        response = self.wait()
        """Response should have no error"""
        self.assertIsNone(response.error)
        """Response code should be 200"""
        self.assertEqual(self._successCode, response.code)
        """Response body type should be str"""
        self.assertEqual(str, type(response.body))
        """
            Make sure there are no <p> tweets present on home page.
            NOTE: GET to '/search' is also redirected to home page.
        """
        parser = responseHTMLParser(self.homeParserCallback)
        parser.feed(response.body)
        parser.close()
        
    """Test requests to '/' path"""
    def test_HomeHandler(self):
        self.defaultHandler("/")
    
    """Test requests to '/search' path"""    
    def test_SearchGETHandler(self):
        self.defaultHandler("/search")

"""Testing common utils from main.py"""
class mainTest(unittest.TestCase):
    def setUp(self):
        self.app_dir = os.path.abspath(os.path.dirname(__file__))

    """getAbsolutePath from main.py that intelligently joins a number of path fragments"""
    def test_getAbsolutePath(self):
        self.assertEqual(self.app_dir + "/some.file", getAbsolutePath("some.file"))
        self.assertEqual(self.app_dir + "/test/some.file", getAbsolutePath("test/some.file"))
        self.assertEqual("/etc/some.file", getAbsolutePath("/etc/some.file"))
        
"""Testing AppRequestHandler class from main.py"""
class AppRequestHandlerTest(unittest.TestCase):
    """test buildRequestUrl that builds url from base and query params."""
    def test_buildRequestUrl(self):
        self.assertEqual("some_url?q=query", AppRequestHandler.buildRequestUrl("some_url", q="query"))
        self.assertEqual("some_url", AppRequestHandler.buildRequestUrl("some_url"))
        self.assertEqual("some_url?q=test&lang=en&v=1.0", AppRequestHandler.buildRequestUrl("some_url", q="test", lang="en", v="1.0"))

"""A mock up of the response object"""
class responseMock(object):
    def __init__(self, error):
        self.error = error

"""Testing AppRequestHandler class from main.py"""
class AsyncHandlerTest(unittest.TestCase):
    def setUp(self):
        self.handler = AsyncHandler()
        self.errorResponse = responseMock(True)

    def test_AsyncHandlere(self):
        with self.assertRaises(tornado.web.HTTPError):
            self.handler.on_response(self.errorResponse)
        self.assertIsNone(self.handler.handleRequestCallback("Test Data"))


if __name__ == "__main__":
    unittest.main()