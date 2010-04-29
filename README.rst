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

Then, you can either go to the admin interface to set up the tokens and websites
you want to use. For this purpose, you need to have an existant admin instance
in your application.

You also can use the `oauth_createtoken` command ::

    $ python manage.py oauthcreatetoken


Setting up the constants
-------------------------

You also need to set up your session key in your settings. It need to be unique
within all your applications::

    PERSISTENT_SESSION_KEY = 'unique persistant session key'


Urls
----
    
Now, you need to provide urls to access the oauthclient application, for your
project. Here is a simple configuration::
    
    urlpatterns = patterns('',
        # your already existing urls
        (r'^oauth/', include('oauthclient.urls', namespace='oauth',
                app_name='yourappoauth'), {'identifier': 'yourappname'}),
    )

