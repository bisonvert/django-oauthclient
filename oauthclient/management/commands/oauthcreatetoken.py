"""
Management utility to create OAuth tokens

"""
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

from oauthclient.models import OAuthServer, ConsumerToken

DEFAULT_REQUEST_TOKEN_URL = '/oauth/request_token/'
DEFAULT_ACCESS_TOKEN_URL = '/oauth/access_token/'
DEFAULT_AUTHORIZE_URL = '/oauth/authorize/'

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--identifier', dest='identifier', default=None, 
            help='Specify an identifier to identify the token later. A good' \
                'idea is to enter the name of the service, or the OAuth' \
                'server.'),
        make_option('--key', dest='key', default=None, 
            help='Specify the OAuth token key.'),
        make_option('--secret', dest='secret', default=None,
            help='Specify the OAuth token secret.'), 
        make_option('--serverurl', dest='serverurl', default=None, 
            help='Specify the OAuth server root url.'),
        make_option('--request-token-url', dest='request_token_url',
            default=DEFAULT_REQUEST_TOKEN_URL, 
            help='Specify the request token url. Default is %s' % DEFAULT_REQUEST_TOKEN_URL),
        make_option('--access_token_url', dest = 'access_token_url',
            default=DEFAULT_ACCESS_TOKEN_URL,
            help='Specify the access token url. Default is %s' % DEFAULT_ACCESS_TOKEN_URL),
        make_option('--authorize-url', dest = 'authorize_url', 
            default=DEFAULT_AUTHORIZE_URL, 
            help='Specify the authorize url. Default is %s' % DEFAULT_AUTHORIZE_URL),
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind. '    \
                 'You must use --server-url, --key and --secret with --noinput.')
    )

    help = 'Used to specify OAuth access urls and token (key & secret).'

    def handle(self, *args, **options):
        identifier = options.get('identifier', None)
        key = options.get('key', None)
        secret = options.get('secret', None)
        server_url = options.get('serverurl', None)
        request_token_url = options.get('request_token_url')
        access_token_url = options.get('access_token_url')
        authorize_url = options.get('authorize_url')
        interactive = options.get('interactive')

        if not interactive:
            if not key or not secret or not server_url:
                raise CommandError("You must use --server-url, --key and" \
                    "--secret with --noinput")

        if interactive:
            if not identifier:
                identifier = raw_input('Token identifier: ')
            if not key:
                key = raw_input('Token key: ')
            if not secret:
                secret = raw_input('Token secret: ')
            if not server_url:
                server_url = raw_input('Server URL: ')
            if not request_token_url:
                request_token_url = raw_input('Request token URL (without server '\
                    'URL prefix): ')
            if not access_token_url:
                access_token_url = raw_input('Access token URL (without server '\
                    'URL prefix): ')
            if not authorize_url:
                authorize_url = raw_input('Authorize URL (without server '\
                    'URL prefix): ')

        server = OAuthServer(server_url=server_url, 
            request_token_url=request_token_url,
            access_token_url=access_token_url,
            authorize_url=authorize_url)
        server.save()

        token = ConsumerToken(identifier=identifier, key=key, secret=secret, server=server)
        token.save()
        print "Consumer Token and Server successfully configured"
