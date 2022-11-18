from datetime import datetime
import json

from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.utils.translation import gettext as _

from comment.models import Comment
from story.models import Story, LikeStatus
from user.models import UserProfile
from utils.get_lang import get_lang_code, translate
from utils.logging_check import logging_check, get_user_by_request


# code 10300-10399    used: 10300-10311
# Create your views here.
def get_story(request, lang_code, username):
    cur_language = get_lang_code(request)
    story_id = request.GET.get('story_num', 0)
    visit_story = request.GET.get('visit_story', False)
    try:
        author = UserProfile.objects.get(username=username)
    except Exception as e:
        message = _('Author does not exist!')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10300, 'msg': t_message})

    if not story_id:
        message = _('Story is not specified!')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10301, 'msg': t_message})
    try:
        story = Story.objects.get(id=story_id)
    except Exception as e:
        message = _('Story does not exist!')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10302, 'msg': t_message})

    if visit_story:
        story.view = story.view + 1
        story.save()

    story_obj = {}
    story_obj['author'] = author.first_name + ' ' + author.last_name
    story_obj['id'] = story.id
    story_obj['title'] = story.title
    story_obj['area'] = story.area
    story_obj['category'] = story.category
    story_obj['country'] = story.country
    story_obj['photo'] = str(story.photo)
    story_obj['photo_desc'] = story.photo_desc
    story_obj['content'] = story.content
    story_obj['view'] = story.view

    total_likes = LikeStatus.objects.filter(story=story, is_clicked=True)
    story_obj['like'] = len(total_likes)
    login_user = get_user_by_request(request)
    if login_user:
        like_status = LikeStatus.objects.filter(user=login_user, story=story).first()
        if not like_status:
            like_status = LikeStatus.objects.create(user=login_user, story=story, is_clicked=False)
            story_obj['like_status'] = like_status.is_clicked
        story_obj['like_status'] = like_status.is_clicked
    else:
        story_obj['like_status'] = False
    story_obj['created_time'] = story.created_time.strftime("%Y-%m-%d  %H:%M:%S")

    comments = Comment.objects.filter(story_id=story_id)
    story_obj['comment'] = len(comments)

    return JsonResponse({'code': 200, 'data': story_obj})


@logging_check
def post_story(request, lang_code, username):
    user = request.login_user
    photo = request.FILES['photo']
    title = request.POST['title']
    area = request.POST['area']
    category = request.POST['category']
    country = request.POST['country']
    photo_desc = request.POST['photo_desc']
    content = request.POST['content']

    story = Story.objects.create(title=title, area=area, category=category, country=country, photo_desc=photo_desc,
                                 content=content, photo=photo, author=user, updated_time=datetime.now())

    return JsonResponse({'code': 200})


@logging_check
def update_story(request, lang_code, username):
    cur_language = get_lang_code(request)

    story_id = request.GET.get('story_num', 0)
    photo = request.FILES.get('photo', '')
    title = request.POST.get('title', '')
    area = request.POST.get('area', '')
    category = request.POST.get('category', '')
    country = request.POST.get('country', '')
    photo_desc = request.POST.get('photo_desc', '')
    content = request.POST.get('content', '')

    print('username', username)
    try:
        author = UserProfile.objects.get(username=username)
    except Exception as e:
        message = _('Author does not exist!')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10304, 'msg': t_message})

    if not story_id:
        message = _('Story to be updated is not specified.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10305, 'msg': t_message})
    try:
        story = Story.objects.get(id=story_id)
    except Exception as e:
        message = _('Story to be updated does not exist.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10306, 'msg': t_message})

    story.title = title
    story.area = area
    story.category = category
    story.country = country
    story.photo_desc = photo_desc
    story.content = content
    if photo != '':
        story.photo = photo
    time = datetime.now()
    story.updated_time = time
    story.save()

    return JsonResponse({'code': 200})


@logging_check
def delete_story(request, lang_code, username):
    cur_language = get_lang_code(request)
    story_id = request.GET.get('story_num', 0)
    if not story_id:
        message = _('Story to be deleted is not specified.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10310, 'msg': t_message})
    try:
        story = Story.objects.get(id=story_id)
    except Exception as e:
        message = _('Story to be deleted does not exist.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10311, 'msg': t_message})

    story.delete()

    user = request.login_user
    stories = Story.objects.filter(author=user)
    page_size = 3
    paginator = Paginator(stories, page_size)
    total_pages = paginator.num_pages

    return JsonResponse({'code': 200, 'total_pages': total_pages})


# for four different areas
def destination_stories(request, lang_code):
    cur_language = get_lang_code(request)
    destination = request.GET.get('destination', '')
    if destination == '':
        message = _('Destination is not specified.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10307, 'msg': t_message})

    page_num = request.GET.get('page_num', 1)
    page_size = 9
    stories = Story.objects.filter(area=destination).order_by('-created_time')
    if not stories:
        message = _('There are no stories for this destination.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10308, 'msg': t_message})
    paginator = Paginator(stories, page_size)

    try:
        data = custom_paginator(stories, page_num, page_size)
    except PageNotAnInteger:
        data = custom_paginator(stories, 1, page_size)
    except EmptyPage:
        data = custom_paginator(stories, paginator.num_pages, page_size)

    return JsonResponse({'code': 200, 'data': data})


@logging_check
def stories_list(request, lang_code, username):
    user = request.login_user
    page_num = request.GET.get('page_num', 1)  # 10 stories/page
    stories = Story.objects.filter(author=user).order_by('-created_time')
    page_size = 10
    paginator = Paginator(stories, page_size)
    try:
        data = custom_paginator(stories, page_num, page_size)
    except PageNotAnInteger:
        data = custom_paginator(stories, 1, page_size)
    except EmptyPage:
        data = custom_paginator(stories, paginator.num_pages, page_size)

    return JsonResponse({'code': 200, 'data': data})


@logging_check
def like_story(request, lang_code, username):
    cur_language = get_lang_code(request)
    data = json.loads(request.body)
    story_id = data.get('story_id', 0)
    like_status = data.get('like_status', '')
    user = request.login_user

    if not story_id:
        message = _('Story to be liked is not specified.')
        t_message = translate(cur_language, message)
        return JsonResponse({'code': 10309, 'msg': t_message})

    like = LikeStatus.objects.filter(user=user, story_id=story_id).first()
    if like_status == 'like':
        like.is_clicked = True
        like.save()
        data = {
            'cur_status': 'unlike',
        }
    else:
        like.is_clicked = False
        like.save()
        data = {
            'cur_status': 'like',
        }

    return JsonResponse({'code': 200, 'data': data})


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
        item['created_time'] = story.created_time.strftime("%Y-%m-%d")
        item['updated_time'] = story.updated_time.strftime("%Y-%m-%d")
        page_of_stories.append(item)

    # 封装一下数据
    data = {
        # 注意这里得到的当前页码的数据列表是QuerySet，不能直接返回前端，会报错
        # 还需要拿到data后简单转换一下
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
