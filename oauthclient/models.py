from django.db import models

KEY_SIZE = SECRET_SIZE = 16

class OAuthServer(models.Model):
    """Defines the urls to use for the oauth authentication.

    """
    server_url = models.URLField(verify_exists = False)
    request_token_url = models.CharField(max_length=300)
    access_token_url = models.CharField(max_length=300)
    authorize_url = models.CharField(max_length=300) 

class Token(models.Model):
    """Define a couple key-secret provided by the oauth server for this
    application.

    """
    identifier = models.CharField(max_length=200, unique=True)
    key = models.CharField(max_length=KEY_SIZE, null=True, blank=True)
    secret = models.CharField(max_length=SECRET_SIZE, null=True, blank=True)
    server = models.ForeignKey(OAuthServer)
    last_modification = models.DateField(auto_now=True)
    
    class Meta:
        get_latest_by = 'last_modification'
