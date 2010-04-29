from django.conf.urls.defaults import *
from views import get_request_token, access_token_ready, logout

urlpatterns = patterns('',
    (r'^request_token/$', get_request_token, {}, 'login'),
    (r'^request_token/$', get_request_token, {}, 'request_token'),
    (r'^access_token_ready/$', access_token_ready, {}, 'access_token_ready'),
    (r'^logout/$', logout, {}, 'logout'),
)
