from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

import requests, json, unidecode, random, uuid


# Google Oauth 2.0 server https://accounts.google.com/o/oauth2/v2/auth
# Google exchange token https://oauth2.googleapis.com/token
@api_view(['GET'])
def googleAuthURL(request):
    google = _get_google()
    authorization_url, state = google.authorization_url(
        access_type='offline', include_granted_scopes='false')
    return redirect(authorization_url)

@api_view(['GET'])
def googleAuth(request):
    error = request.GET.get('error', None) 
    if not error:
        google = _get_google()
        google.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = google.credentials
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        print(user_info)
        validated_data, avatar_url = validateGoogleInfo(user_info)
        serializer = UserSerializer(data=validated_data)
        if serializer.is_valid():
            user = serializer.save()
            userProfile = user.profile
            userProfile.avatar_url = avatar_url
            userProfile.verified = True
            userProfile.save()
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response({'message': "Signup with google successfully", 'data': token})
        message = ""
        for key, value in serializer.errors.items():
            message += f'{value[0]} ({key})'
            break
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def facebookAuthURL(request):
    facebook = _get_facebook()
    authorization_base_url = 'https://www.facebook.com/v18.0/dialog/oauth'
    authorization_url, state = facebook.authorization_url(authorization_base_url)
    return redirect(authorization_url)

@api_view(['GET'])
def facebookAuth(request):
    error = request.GET.get('error', None) 
    if not error:
        facebook = _get_facebook()
        facebook.fetch_token(authorization_response=request.build_absolute_uri(),
                            token_url='https://graph.facebook.com/oauth/access_token', 
                            client_secret=settings.FACEBOOK_CLIENT_SECRET)
        res = facebook.get('https://graph.facebook.com/me?fields=id,name,email,first_name,last_name,picture.width(640)')
        user_info = json.loads(res.content.decode())
        validated_data, avatar_url = validateFacebookInfo(user_info)
        serializer = UserSerializer(data=validated_data)
        if serializer.is_valid():
            user = serializer.save()
            userProfile = user.profile
            userProfile.avatar_url = avatar_url
            userProfile.verified = True
            userProfile.save()
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response({'message': "Signup with facebook successfully", 'data': token})
        message = ""
        for key, value in serializer.errors.items():
            message += f'{value[0]} ({key})'
            break
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST)



def validateFacebookInfo(user_info):
    validated_data = {
        'username': _generate_username(user_info['name']),
        'email': user_info.get('email', ''),
        'password': str(uuid.uuid4()),
        'first_name': user_info.get('first_name', 'schat'),
        'last_name': user_info.get('last_name', 'schat'),
    }
    avatar_url = user_info['picture']['data']['url']
    return validated_data, avatar_url


def validateGoogleInfo(user_info):    
    validated_data = {
        'username': _generate_username(user_info['name']),
        'email': user_info.get('email', ''),
        'password': str(uuid.uuid4()),
        'first_name': user_info.get('given_name', 'schat'),
        'last_name': user_info.get('family_name', 'schat'),
    }
    avatar_url = user_info['picture']
    return validated_data, avatar_url


def _generate_username(name):
    name = unidecode.unidecode(name.replace(' ', '')).lower()
    suffix = ""
    if (len(name) < 6):
        name += '0' * (6 - len(name))
    while User.objects.filter(username=(f'{name}{suffix}')).exists():
        suffix = random.randint(1, 99)
        if suffix < 10: suffix = f'0{suffix}'
    return f'{name}{suffix}'

def _get_google():
    google = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config=settings.GOOGLE_CONFIG,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
        scopes=['email', 'profile'])
    return google

def _get_facebook():
    facebook = OAuth2Session(
        client_id=settings.FACEBOOK_CLIENT_ID,
        redirect_uri=settings.FACEBOOK_REDIRECT_URI,
        scope=['email', 'public_profile'])
    facebook = facebook_compliance_fix(facebook)
    return facebook