from django.db.models import get_models, signals
from oauthclient import models as oauthclient_app
from django.core.management import call_command

def create_oauth_token(app, created_models, verbosity, **kwargs):
    from oauthclient.models import ConsumerToken
    if ConsumerToken in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed oauthclient app, wich means you" \
                "don't have any consumer token defined yet.\n Would you like to define " \
                "them now ? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                call_command("oauthcreatetoken", interactive=True)
            break

#signals.post_syncdb.connect(create_oauth_token, sender=oauthclient_app,
#    dispatch_uid="oauthclient.management.create_oauth_token")
