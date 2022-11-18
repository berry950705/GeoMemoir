from django.utils.translation import gettext, activate

from geo_memoir import settings


def get_lang_code(request):
    request_url = request.path_info
    request_language = request_url.split('/')[2]

    cur_language = None
    if request_language == 'zh_Hant_TW':
        cur_language = 'zh_TW'
    elif request_language == 'zh_Hans_CN':
        cur_language = 'zh_CN'

    if cur_language not in settings.LANGUAGES_LIST:
        cur_language = 'en'

    return cur_language


def translate(cur_language, message):
    activate(cur_language)
    text = gettext(message)
    return text
