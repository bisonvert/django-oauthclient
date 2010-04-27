""" To be managed in django admin"""
from oauthclient.models import OAuthServer, ConsumerToken
from django.contrib import admin

admin.site.register(OAuthServer)
admin.site.register(ConsumerToken)
