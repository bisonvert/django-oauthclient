#django imports
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from models import ConsumerToken, OAuthServer

def get_consumer_token(identifier):
    return ConsumerToken.objects.get(identifier=identifier)

def oauth_need_authentication(request, identifier, force=False):
    """Authenticate user using oauth flow, if the an authentication does not
    already exists.
    
    """
    return not (identifier + '_oauth_token' and identifier + '_oauth_token_secret' in request.session)
    
def is_oauthenticated(identifier, force=False):
    """Decorator when oauth authentication is needed.
    
    If the user is not authenticated, redirect the user to the oauth 
    authentication flow.
    
    Use this decorator with django views, like this::
        
        @is_oauthenticated()
        def myview(request):
            pass
    """
    def wrapper(func):
        def wrapped(*args, **kwargs):
            request = args[0]
            if force or oauth_need_authentication(request=request,
                    identifier=identifier, force=force):
                return redirect('%s?next=%s' % (
                    reverse('oauth:request_token'), 
                    request.path))
            else:
                return func(*args, **kwargs)
        return wrapped
    return wrapper
