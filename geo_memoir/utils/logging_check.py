import jwt
from django.conf import settings
from django.http import JsonResponse
from user.models import UserProfile


def logging_check(func):
    def wrap(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'code': 403, 'msg': 'Please log in to continue!'})

        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'msg': 'Token has expired. Please log in again!'})

        # get log_in user
        username = res['username']
        user = UserProfile.objects.get(username=username)
        request.login_user = user
        return func(request, *args, **kwargs)
    return wrap


def get_user_by_request(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    if not token:
        return None
    try:
        jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        print('Token has expired!')
        return None

    res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms='HS256')
    username = res['username']
    user = UserProfile.objects.get(username=username)
    return user



