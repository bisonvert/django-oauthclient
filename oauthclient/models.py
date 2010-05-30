from django.db import models
from django.conf import settings
from oauthclient.settings import CONSUMER_KEY_SIZE, CONSUMER_SECRET_SIZE
import oauth2

class OAuthServer(models.Model):
    """Defines the urls to use for the oauth authentication.

    """
    server_url = models.URLField(verify_exists = False)
    request_token_url = models.CharField(max_length=300)
    access_token_url = models.CharField(max_length=300)
    authorize_url = models.CharField(max_length=300)

    def get_request_token_url(self):
        return self.server_url + self.request_token_url

    def get_access_token_url(self):
        return self.server_url + self.access_token_url
    
    def get_authorize_url(self):
        return self.server_url + self.authorize_url

    def __unicode__(self):
        return u'Server : %s' % self.server_url

    class Meta:
        verbose_name = "OAuth Server"


class ConsumerToken(models.Model):
    """Define a couple key-secret provided by the oauth server for this
    application.

    """
    identifier = models.CharField(max_length=200, unique=True)
    key = models.CharField(max_length=CONSUMER_KEY_SIZE, null=True, blank=True)
    secret = models.CharField(max_length=CONSUMER_SECRET_SIZE, null=True, blank=True)
    server = models.ForeignKey(OAuthServer)
    last_modification = models.DateField(auto_now=True)

    def __unicode__(self):
        return 'Token : %s' % self.identifier

    def get_consumer(self):
        """Return a consumer object, configured with settings values.
        
        """
        return oauth2.Consumer(self.key, self.secret)
    
    class Meta:
        get_latest_by = 'last_modification'
