import hashlib
import json
import time
import jwt
from django.http import JsonResponse
from django.utils.translation import gettext as _
from google.auth.transport import requests
from google.oauth2 import id_token

from geo_memoir import settings
from user.models import UserProfile
from utils.get_lang import get_lang_code, translate


# error_code : 10100-10199   used: 10100 - 10103
# Create your views here.


def make_token(username, expire=86400):
    payload = {'username': username, 'exp': time.time() + expire}
    token = jwt.encode(payload=payload, key=settings.JWT_TOKEN_KEY, algorithm='HS256')
    return token.decode()


def tokens(request, lang_code):
    """
    login token
    """
    # get current language
    cur_language = get_lang_code(request)

    if request.method != 'POST':
        result = {'code': 10100, 'msg': 'POST method is required!'}
        return JsonResponse(result)

    json_obj = json.loads(request.body)
    username = json_obj['username']
    password = json_obj['password']

    # validate username and password
    user = UserProfile.objects.filter(username=username).first()
    if not user:
        message = _('Username or password is wrong.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10101, 'msg': t_message})

    m = hashlib.md5()
    m.update(password.encode())
    password_m = m.hexdigest()
    if password_m != user.password:
        message = _('Username or password is wrong')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10102, 'msg': t_message})

    # issue token
    token = make_token(username)

    return JsonResponse({'code': 200, 'username': username, 'token': token})


def google_token(request, lang_code):
    cur_language = get_lang_code(request)

    data = json.loads(request.body)
    google_token = data['google_token']
    user_info = id_token.verify_oauth2_token(google_token, requests.Request(), audience=settings.GOOGLE_CLIENT_ID)
    google_id = user_info['sub']
    picture = user_info['picture']
    first_name = user_info['given_name']
    last_name = user_info['family_name']
    email = user_info['email']

    # check if the user has logged in before
    user = UserProfile.objects.filter(google_id=google_id).first()
    if user:
        username = user.username
        token = make_token(username)
        return JsonResponse({'code': 200, 'username': username, 'token': token})

    # create new userprofile if no user
    else:
        # check first if the email has been registered already
        registered_email = UserProfile.objects.filter(email=email)
        if registered_email:
            message = _('This email has already been registered.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10103, 'msg': t_message})

        u_time = str(int(time.time()))
        u_id = str(google_id)[-5:]
        username = u_time + u_id

        UserProfile.objects.create(google_id=google_id, google_pic=picture, username=username, first_name=first_name,
                                   last_name=last_name, email=email)

        print({
            'google_id': google_id,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'picture': picture,
        })

        token = make_token(username)
        return JsonResponse({'code': 200, 'username': username, 'token': token})
