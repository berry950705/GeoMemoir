import base64
import hashlib
import json
import re
import time
import random

import jwt
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.http import JsonResponse

from utils.get_lang import get_lang_code, translate
from .tasks import *
from django.utils.translation import gettext as _

from geo_memoir import settings
from user.models import UserProfile
from story.models import Story, LikeStatus
from utils.logging_check import *
from django.shortcuts import render


# error_code: 10200-10299    used: 10200 - 10227
# Create your views here.


class UserViews(View):
    def get(self, request, lang_code, username=None):
        cur_language = get_lang_code(request)

        if not username:
            message = _('User is not defined.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10200, 'msg': t_message})

        else:
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                print('Get profile error:', e)
                message = _('User does not exist!')
                t_message = translate(cur_language, message)
                JsonResponse({'code': 10201, 'msg': t_message})

            # author's travel profile info
            total_stories = Story.objects.filter(author=user)
            area_count1 = Story.objects.filter(author=user, area='The Americas')
            area_count2 = Story.objects.filter(author=user, area='Asia Pacific')
            area_count3 = Story.objects.filter(author=user, area='Europe')
            area_count4 = Story.objects.filter(author=user, area='Middle East / Africa')
            visited_count = Story.objects.filter(author=user).values('country').distinct()

            author = {}
            if user.background_img:
                author['background_img'] = str(user.background_img)
            if user.avatar:
                author['avatar'] = str(user.avatar)
            author['username'] = user.username
            author['profile_name'] = user.profile_name
            author['motto'] = user.motto
            author['self_intro'] = user.self_intro
            author['total_stories'] = len(total_stories)
            author['area_count1'] = len(area_count1)
            author['area_count2'] = len(area_count2)
            author['area_count3'] = len(area_count3)
            author['area_count4'] = len(area_count4)
            author['visited_count'] = len(visited_count)

            # make author's stories_list
            page_num = request.GET.get('page_num', 1)
            page_size = 9
            stories = Story.objects.filter(author=user).order_by('-created_time')
            paginator = Paginator(stories, page_size)

            try:
                data = custom_paginator(stories, page_num, page_size)
            except PageNotAnInteger:
                data = custom_paginator(stories, 1, page_size)
            except EmptyPage:
                data = custom_paginator(stories, paginator.num_pages, page_size)

            return JsonResponse({'code': 200, 'data': {'author': author, 'stories_data': data}})

    def post(self, request, lang_code, username=None):
        cur_language = get_lang_code(request)
        data = json.loads(request.body)
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        username = data.get('username', '')
        email = data.get('email', '')
        password1 = data.get('password1', '')
        password2 = data.get('password2', '')

        # regex for username, email, password
        username_regex = r'^[a-zA-Z0-9]{6,}$'
        email_regex = r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
        pwd_reg1 = r'[A-Z]'
        pwd_reg2 = r'[a-z]'
        pwd_reg3 = r'[0-9]'
        re_reg1 = re.search(pwd_reg1, password1)
        re_reg2 = re.search(pwd_reg2, password1)
        re_reg3 = re.search(pwd_reg3, password1)

        if not first_name:
            message = _('First name is empty!')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10202, 'msg': t_message})
        if not last_name:
            message = _('Last name is empty!')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10203, 'msg': t_message})
        if not re.search(username_regex, username):
            message = _('Invalid username! Please check again.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10204, 'msg': t_message})
        if not re.search(email_regex, email):
            message = _('Invalid email! Please check again.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10205, 'msg': t_message})
        if not re_reg1 or not re_reg2 or not re_reg3 or len(password1) < 8:
            message = _('Invalid password! Please check again.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10206, 'msg': t_message})
        if password1 != password2:
            message = _('Passwords do not match! Please check again.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10207, 'msg': t_message})

        # check if username is available
        current_users = UserProfile.objects.filter(username=username)
        if current_users:
            message = _('Username is not available.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10208, 'msg': t_message})
        current_email = UserProfile.objects.filter(email=email)
        if current_email:
            message = _('This email has already been registered.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10209, 'msg': t_message})

        # convert password into md5
        m = hashlib.md5()
        m.update(password1.encode())
        password_m = m.hexdigest()

        # save data to mysql (考慮併發問題)
        try:
            UserProfile.objects.create(first_name=first_name, last_name=last_name, username=username,
                                       password=password_m,
                                       email=email)
        except Exception as e:
            print('Create user error: %s', e)
            message = _('Username is not available.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10210, 'msg': t_message})

        # issue token
        token = make_token(username)

        # return data
        return JsonResponse({'code': 200, 'username': username, 'token': token})


@logging_check
def edit_profile(request, lang_code, username=None):
    user = request.login_user
    avatar = request.FILES.get('avatar', '')
    bg_img = request.FILES.get('background', '')
    profile_name = request.POST['profile_name']
    motto = request.POST['motto']
    self_intro = request.POST['self_intro']

    if avatar != '':
        user.avatar = avatar
    if bg_img != '':
        user.background_img = bg_img
    user.profile_name = profile_name
    user.motto = motto
    user.self_intro = self_intro
    user.save()
    return JsonResponse({'code': 200})


def make_token(username, expire=86400):
    payload = {'username': username, 'exp': int(time.time()) + expire}
    token = jwt.encode(payload, settings.JWT_TOKEN_KEY, algorithm='HS256')
    return token.decode()


@logging_check
def show_login_account(request, lang_code):
    cur_language = get_lang_code(request)
    user = get_user_by_request(request)
    if not user:
        message = _('Token has expired. Please log in again!')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 401, 'msg': t_message})

    user_data = {}
    google_id = user.google_id
    if google_id:
        user_data['username'] = user.username
        user_data['first_name'] = user.first_name
        user_data['email'] = user.email
        user_data['picture'] = user.google_pic
        return JsonResponse({'code': 200, 'google_user': 'google', 'data': user_data})

    else:
        user_data['username'] = user.username
        user_data['first_name'] = user.first_name
        if user.avatar:
            user_data['avatar'] = str(user.avatar)
        return JsonResponse({'code': 200, 'data': user_data})


def forgot_password(request, lang_code):
    cur_language = get_lang_code(request)
    data = json.loads(request.body)
    email = data.get('email', '')
    try:
        user = UserProfile.objects.get(email=email)
    except Exception as e:
        message = _('This email has not been registered. Please check again.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10211, 'msg': t_message})
    username = user.username
    recipient = user.first_name + ' ' + user.last_name
    try:
        ran_num = random.randint(10000, 99999)
        code_str = '%s_%s' % (ran_num, username)
        b64_code = base64.urlsafe_b64encode(code_str.encode()).decode()
        cache.set('reset_password_%s' % username, ran_num)
        reset_url = 'https://geomemoir.fun/' + lang_code + '/reset_password?code=%s' % b64_code
        email_password_reset_link.delay(lang_code, email, recipient, str(reset_url))
    except Exception as e:
        print('Sending password reset url error:', e)
        message = _('Server is busy. Please try again later.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10212, 'msg': t_message})
    return JsonResponse({'code': 200})


def reset_password(request, lang_code):
    cur_language = get_lang_code(request)
    # base64decode -> verify ran_num and username
    code = request.GET.get('code', '')
    if not code:
        message = _('Code required for password reset is missing.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10213, 'msg': t_message})
    code_str = base64.urlsafe_b64decode(code.encode()).decode()
    ran_num, username = code_str.split('_')
    old_ran_num = cache.get('reset_password_%s' % username)
    if not old_ran_num:
        message = _('Code has expired!')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10214, 'msg': t_message})
    if int(ran_num) != int(old_ran_num):
        message = _('Code is wrong!')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10215, 'msg': t_message})

    try:
        user = UserProfile.objects.get(username=username)
    except Exception as e:
        message = _('User cannot be found.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10216, 'msg': t_message})

    # verify new password
    data = json.loads(request.body)
    new_pwd = data.get('new_pwd', '')
    confirm_pwd = data.get('confirm_pwd', '')

    if new_pwd != confirm_pwd:
        message = _('Passwords do not match.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10217, 'msg': t_message})

    pwd_reg1 = r'[A-Z]'
    pwd_reg2 = r'[a-z]'
    pwd_reg3 = r'[0-9]'
    re_reg1 = re.search(pwd_reg1, new_pwd)
    re_reg2 = re.search(pwd_reg2, new_pwd)
    re_reg3 = re.search(pwd_reg3, new_pwd)
    if not re_reg1 or not re_reg2 or not re_reg3 or len(new_pwd) < 8:
        message = _('New password is invalid. Please check again.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10218, 'msg': t_message})

    # md5 new password and save
    m_new_pwd = hashlib.md5(new_pwd.encode())
    user.password = m_new_pwd.hexdigest()
    user.save()
    return JsonResponse({'code': 200})


@logging_check
def get_user_email(request, lang_code, username):
    user = request.login_user
    return JsonResponse({'code': 200, 'user_email': user.email})


@logging_check
def send_email_code(request, lang_code, username):
    cur_language = get_lang_code(request)
    user = request.login_user
    data = json.loads(request.body)
    email = data.get('new_email', '')
    old_user = UserProfile.objects.filter(email=email).first()
    if old_user:
        if email == old_user.email:
            message = _('This email has already been registered.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10227, 'msg': t_message})
    code = random.randint(100000, 999999)
    cache.set('change_email_%s' % user.username, code)
    recipient = user.first_name + ' ' + user.last_name
    try:
        send_change_email_code.delay(lang_code, email, recipient, code)
    except Exception as e:
        print('Send email verification code error:', e)
        message = _('Server is busy. Please try again later.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10219, 'msg': t_message})
    return JsonResponse({'code': 200})


@logging_check
def change_email(request, lang_code, username):
    cur_language = get_lang_code(request)
    user = request.login_user
    data = json.loads(request.body)
    email = data.get('new_email', '')
    code = data.get('code', 0)
    if not email or not code:
        message = _('Email or code is missing.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10220, 'msg': t_message})
    old_code = cache.get('change_email_%s' % user.username)
    if not old_code:
        message = _('Code has expired.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10221, 'msg': t_message})

    if int(code) != int(old_code):
        message = _('Code is wrong.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10222, 'msg': t_message})

    user.email = email
    user.save()
    return JsonResponse({'code': 200})


@logging_check
def change_password(request, lang_code, username):
    cur_language = get_lang_code(request)
    user = request.login_user
    data = json.loads(request.body)
    old_pwd = data.get('old_pwd', '')
    new_pwd = data.get('new_pwd', '')
    confirm_pwd = data.get('pwd_confirm', '')

    if not old_pwd or not new_pwd or not confirm_pwd:
        message = _('Information required to change the password is incomplete.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10223, 'msg': t_message})

    m_old_pwd = hashlib.md5(old_pwd.encode())
    if m_old_pwd.hexdigest() != user.password:
        message = _('Old password is wrong!')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10224, 'msg': t_message})

    # verify new password
    if new_pwd != confirm_pwd:
        message = _('Passwords do not match.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10225, 'msg': t_message})

    pwd_reg1 = r'[A-Z]'
    pwd_reg2 = r'[a-z]'
    pwd_reg3 = r'[0-9]'
    re_reg1 = re.search(pwd_reg1, new_pwd)
    re_reg2 = re.search(pwd_reg2, new_pwd)
    re_reg3 = re.search(pwd_reg3, new_pwd)

    if not re_reg1 or not re_reg2 or not re_reg3 or len(new_pwd) < 8:
        message = _('New password is invalid. Please check again.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10226, 'msg': t_message})

    # md5 new password and save
    m_new_pwd = hashlib.md5(new_pwd.encode())
    user.password = m_new_pwd.hexdigest()
    user.save()
    return JsonResponse({'code': 200})


def custom_paginator(obj, page, page_size):
    paginator = Paginator(obj, page_size)  # 将接收到的obj变量按照page_size分页
    page_of_obj = paginator.page(page)  # 得到当前page的数据列表  <Page 1 of 2>
    page_of_obj_list = page_of_obj.object_list  # get data in list ['john', 'paul']
    current_page_num = page_of_obj.number  # 当前页码 num
    has_previous = page_of_obj.has_previous()  # 上一页 True
    has_next = page_of_obj.has_next()  # 下一页 True
    total_page = paginator.num_pages  # 总页数 num
    count = paginator.count  # 数据记录总数 num

    # 这里判断左右两边的页码小于最小页数或大于最大页数
    if current_page_num - 1 <= 0:
        previous_page_num = 1
    else:
        previous_page_num = current_page_num - 1

    if current_page_num + 1 >= total_page:
        next_page_num = total_page
    else:
        next_page_num = current_page_num + 1

    if current_page_num * page_size - page_size == 0:  # 當頁第一條數據在總數據的排序
        current_start_num = 1
    else:
        current_start_num = current_page_num * page_size - page_size
    if current_page_num * page_size > count:  # 當頁最後一條數據在總數據的排序
        current_end_num = count
    else:
        current_end_num = current_page_num * page_size

    # convert QuerySet data to list
    page_of_stories = []
    for story in page_of_obj_list:
        item = {}
        item['username'] = story.author.username
        item['id'] = story.id
        item['title'] = story.title
        item['area'] = story.area
        item['country'] = story.country
        item['category'] = story.category
        item['photo'] = str(story.photo)
        item['photo_desc'] = story.photo_desc
        item['view'] = story.view
        total_likes = LikeStatus.objects.filter(story=story, is_clicked=True)
        item['like'] = len(total_likes)
        item['created_time'] = story.created_time.strftime("%Y-%m-%d  %H:%M:%S")
        item['updated_time'] = story.updated_time.strftime("%Y-%m-%d  %H:%M:%S")
        page_of_stories.append(item)

    # 封装一下数据
    data = {
        # 'objects_list': page_of_obj,
        'stories_in_list': page_of_stories,
        'has_previous': has_previous,
        'has_next': has_next,
        'current_page_num': current_page_num,
        'previous_page_num': previous_page_num,
        'next_page_num': next_page_num,
        'current_start_num': current_start_num,
        'current_end_num': current_end_num,
        'total_page': total_page,
        'count': count,
    }

    return data
