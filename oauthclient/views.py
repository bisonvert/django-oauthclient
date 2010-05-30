# django imports
from django.shortcuts import render_to_response, redirect
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

# oauth imports
import oauth2
import urlparse

#oauthclient import
from models import ConsumerToken, OAuthServer
from oauthclient import settings

"""These views are a generic way to do a three legged authentication with OAuth. 

You can find more information on three legged authentication on the OAuth
website: http://oauth.net/core/diagram.png

"""

def get_request_token(request, identifier='default'):
    """First and second step of the three-legged OAuth flow:
    
    Request a request token to the OAuth server, and redirect the user on the
    OAuth server, to authorize user access, aka steps A, B and C.
    
    Once this done, the server redirect the user on the access_token_ready
    view.
    
    """
    token = ConsumerToken.objects.get(identifier=identifier)
    client = oauth2.Client(token.get_consumer())
    resp, content = client.request(token.server.get_request_token_url(), "GET")

    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])    

    request_token = dict(urlparse.parse_qsl(content))
    if not ('oauth_token' and 'oauth_token_secret' in request_token):
        raise Exception("Invalid response: oauth_token and oauth_token_secret have to be present in the OAuth server response")
    
    # store information in session
    request.session[identifier + '_request_token'] = request_token['oauth_token']
    request.session[identifier + '_request_token_secret'] = request_token['oauth_token_secret']
    
    #redirect the user to the authentication page
    callback_url = 'http://%s%s' % (
        Site.objects.get_current().domain, 
        reverse('oauth:access_token_ready'))
    
    redirect_url = "%s?oauth_token=%s&oauth_callback=%s" % (
        token.server.get_authorize_url(), 
        request_token['oauth_token'], 
        callback_url)

    if 'next' in request.GET:
        request.session['next'] = request.GET['next']
    request.session.save()
    return redirect(redirect_url)
    
def access_token_ready(request, identifier='default'):
    """Last step of the OAuth three-legged flow.

    The user is redirected here once he allowed (or not) the application to 
    access private informations, aka steps D, E and F.
    
    Echange a valid request token against a valid access token. If a valid 
    access token is given, store it in session.
    
    """
    if not identifier+'_request_token' and identifier+'_request_token_secret' in request.session:
        raise Exception('%s_request_token and %s_request_token_secret are not' \
            'present in session.' % (identifier, identifier))
    
    if ('error' in request.GET):
        return render_to_response(settings.ERROR_TEMPLATE, {
            'error':request.GET['error']
        })
    
    if not 'oauth_verifier' in request.GET:
        raise Exception('oauth_verifier must be present in request.GET')
    
    token = ConsumerToken.objects.get(identifier=identifier)

    # Echange the request token against a access token.
    request_token = oauth2.Token(request.session[identifier + '_request_token'],
        request.session[identifier + '_request_token_secret'])
    request_token.set_verifier(request.GET['oauth_verifier'])
    client = oauth2.Client(token.get_consumer(), request_token)
    resp, content = client.request(token.server.get_access_token_url() , "POST")
    access_token = dict(urlparse.parse_qsl(content))
    
    # test if access token is valid. 
    if not ('oauth_token' and 'oauth_token_secret' in access_token):
        raise Exception('oauth_token and oauth_token_secret must be present in the OAuth server response')
        
    request.session[identifier + '_oauth_token'] = access_token['oauth_token']
    request.session[identifier + '_oauth_token_secret'] = access_token['oauth_token_secret']

    if 'next' in request.session:
        return redirect(request.session['next'])
    if settings.REDIRECT_AFTER_LOGIN == None:
        return render_to_response(settings.LOGIN_TEMPLATE)
    return redirect(settings.REDIRECT_AFTER_LOGIN)
    
def logout(request, identifier='default'):
    """Destruct the active session oauth related keys.
    
    """
    for key in ('oauth_token', 'oauth_token_secret', 
        'request_token', 'request_token_secret'):
        if identifier + '_' + key in request.session:
            del request.session[identifier + '_' + key]
    request.session.save()
    if settings.REDIRECT_AFTER_LOGOUT == None:
        return render_to_response(settings.LOGOUT_TEMPLATE)
    return redirect(settings.REDIRECT_AFTER_LOGOUT)
