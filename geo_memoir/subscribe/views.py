import json
import re

from django.http import JsonResponse
from django.utils.translation import gettext as _

from subscribe.models import Subscribe
from utils.get_lang import get_lang_code, translate


# error code: 10700 - 10701
# Create your views here.
def subscribe_info(request, lang_code):
    cur_language = get_lang_code(request)
    data = json.loads(request.body)
    name = data.get('name', '')
    email = data.get('email', '')

    if not name or not email:
        message = _('Information is incomplete.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10700, 'msg': t_message})

    email_regex = r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    if not re.search(email_regex, email):
        message = _('Invalid email! Please check again.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10701, 'msg': t_message})

    Subscribe.objects.create(name=name, email=email)
    return JsonResponse({'code': 200})
