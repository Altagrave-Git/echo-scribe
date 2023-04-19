from django.shortcuts import render
from .models import CustomUser, OAuth2Token
from authlib.integrations.django_client import OAuth
from django.http import HttpResponse
from django.utils.crypto import get_random_string


def fetch_token(name, request):
    token = OAuth2Token.objects.get(
        name=name,
        user=request.user
    )
    return dict(
        access_token=token.access_token,
        token_type=token.token_type,
        refresh_token=token.refresh_token,
        expires_at=token.expires_at,
        expires_in=token.expires_in,
    )


def update_token(name, token, refresh_token=None, access_token=None):
    if refresh_token:
        item = OAuth2Token.objects.get(name=name, refresh_token=refresh_token)
    elif access_token:
        item = OAuth2Token.objects.get(name=name, access_token=access_token)
    else:
        return
# update old token
    item.access_token = token['access_token']
    item.refresh_token = token.get('refresh_token')
    item.expires_at = token['expires_at']
    item.save()


# Init the OAuth
oauth = OAuth(fetch_token=fetch_token, update_token=update_token)
#oauth = OAuth()
oauth.register(
    name='toolkit',
)

STATE_CODE_LENGTH = 20


def login(request):
    state = get_random_string(STATE_CODE_LENGTH)
    redirect_uri = request.build_absolute_uri('/web/authorize')
    request.session['session_state'] = state
    extra_para = {'state': state}


    return oauth.toolkit.authorize_redirect(request, redirect_uri, **extra_para)#type:ignore


def authorize(request):
    app_state = request.GET.get('state', '')
    session_state = request.session.get('session_state', '')


    if app_state == session_state:
        token = oauth.toolkit.authorize_access_token(request)#type:ignore
        return HttpResponse("welcome")
    else: 
        return HttpResponse("state not match")
