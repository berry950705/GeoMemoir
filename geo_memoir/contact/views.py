import json
import re

from django.http import JsonResponse
from django.utils.translation import gettext as _

from contact.models import Contact
from utils.get_lang import get_lang_code, translate


# error code: 10600 - 10601
# Create your views here.
def contact_info(request, lang_code):
    cur_language = get_lang_code(request)
    data = json.loads(request.body)
    name = data.get('name', '')
    email = data.get('email', '')
    message = data.get('message', '')

    if not name or not email or not message:
        msg = _('Contact information is incomplete.')
        t_msg = translate(cur_language, msg)
        return JsonResponse({'code': 10600, 'msg': t_msg})

    email_regex = r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    if not re.search(email_regex, email):
        msg = _('Invalid email! Please check again.')
        t_msg = translate(cur_language, msg)
        return JsonResponse({'code': 10601, 'msg': t_msg})

    Contact.objects.create(name=name, email=email, message=message)
    return JsonResponse({'code': 200})
