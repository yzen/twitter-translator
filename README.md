Twitter Translate web app.
===

This web app allows users to search for anything on Twitter. The app displays latest 20 tweets that match the search criteria. For every tweet that is not in user's native language there is an option to translate the tweet using Google Translate API.
NOTE: As of December 2011 Google Translate API v1 will stop working so you would have to use v2 API that is not free.


### Dependencies

---
Make sure python (preferably 2.6 or higher) is installed on your machine.

---
Twitter Translate is build using Tornado web server. Below are steps to install Tornado:

Platforms: any Unix-like platform; for best performance and scalability Linux and BSD are recommended.

Manual installation: Download [tornado-2.1.1.tar.gz](http://github.com/downloads/facebook/tornado/tornado-2.1.1.tar.gz).

    tar xvzf tornado-2.1.1.tar.gz
    cd tornado-2.1.1
    python setup.py build
    sudo python setup.py install

Automatic installation: Tornado is listed in PyPI and can be installed with pip or easy_install.
For more information please visit: [Tornado Web Server](http://www.tornadoweb.org/).

### Running
From the checkout directory for Twitter Translate, run

    python src/main.py

or (if you can execute ./src/main.py) simply

    ./src/main.py

Twitter Translate should now run on localhost:8888


### Configuring
Twitter Translate has a config file located at "./src/app.conf". Config file currently contains 3 configurable options:

  - port - port number to run the server on
  - twitterUrl - Twitter url used to search based on user criteria
  - googleTranslateUrl - Google Translate url used to translate tweets
  
### Testing
To run tests, from the checkout directory for Twitter Translate, run

    python src/tests.py
    
or (if you can execute ./src/tests.py) simply

    ./src/tests.py