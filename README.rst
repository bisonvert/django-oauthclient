Django OAuth Client Application
===============================

This application provides a simple way to setup a tree-legged OAuth 
authentication for django.

It has been originally created for the default client of `Bison Vert
<http://www.bisonvert.net>`_.

The code is avalaible under a BSD licence.

Installation
------------

On you django application, add oauthclient to the app list::

    INSTALLED_APPS = (
        # your already installed apps
        'oauthclient',
    )

Please, note that you *need* to use the `django.contrib.site` application,
properly configured with your project default url. This is needed to redirect
the user on you website once authenticated on the distant server.

Then, run syncdb, in order to create the tables that will store the token key
and secrets you'll use for your application.::

    $ python manage.py syncdb

Configuration
--------------

Then, to set up you tokens and oauth providers, you can either go to the admin 
interface (if you have one), or use the `oauthcreatetoken` command, for instance::

    $ python manage.py oauthcreatetoken
    Token identifier: bisonvert
    Token key: wsWLjVsSTPYd8H8xV8
    Token secret: G64F6GNWfKV8kV2DTU66JkFSPKVhhTT9
    Server URL: http://api.bisonvert.net 
    Consumer Token and Server successfully configured


Please note that you need the oauth provider token key and secret, *and* a token
identifier, that represents the associated OAuth provider. it have to match the
one provided in urls (see below). Default is `default`. 

Setting up the constants
-------------------------

In order to prevent cookie based problems between your client and server, 
please check that your `PERSISTENT_SESSION_KEY` settings are *differents* 
in both applications:: 

    PERSISTENT_SESSION_KEY = 'unique persistant session key'

Urls
----
    
Now, you need to provide urls to access the oauthclient application, for your
project. Here is a simple configuration, feel free to adapt to your needs::
    
    urlpatterns = patterns('',
        # your already existing urls
        (r'^oauth/', include('oauthclient.urls', namespace='oauth',
                app_name='yourappoauth'), {'identifier': 'yourappname'}),
    )

