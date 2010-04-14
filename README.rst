Django OAuth Client Application
===============================

A tree-legged OAuth authentication application for django.

Installation
------------

On you django application, add oauthclient to the app list::

    INSTALLED_APPS = (
        # your already installed apps
        'oauthclient',
    )

Then, run syncdb::

    $ python manage.py syncdb

Configuration
-------------

And go to the admin interface to set up the tokens (be sure to activate it.). You also can specify the tokens in your settings file. Here are the constants::

    PERSISTENT_SESSION_KEY = 'unique persistant session key'

    # OAUTH URLs
    OAUTH_SERVER_URL = "the oauth server url"
    OAUTH_REQUEST_TOKEN_URL = '%s/oauth/request_token/' % OAUTH_SERVER_URL
    OAUTH_ACCESS_TOKEN_URL = '%s/oauth/access_token/' % OAUTH_SERVER_URL
    OAUTH_AUTHORIZE_URL = '%s/oauth/authorize/' % OAUTH_SERVER_URL
 
