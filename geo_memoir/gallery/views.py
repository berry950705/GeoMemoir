import base64

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

# error code 10400-10499     used: 10400 - 1040
# Create your views here.
from story.models import Story


def get_photos(request, lang_code):
    page_num = request.GET.get('page_num', 1)
    page_size = 12
    stories = Story.objects.all().order_by('-created_time')
    paginator = Paginator(stories, page_size)
    try:
        data = custom_paginator(stories, page_num, page_size)
    except PageNotAnInteger:
        data = custom_paginator(stories, 1, page_size)
    except EmptyPage:
        data = custom_paginator(stories, paginator.num_pages, page_size)

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
    page_of_photos = []
    for story in page_of_obj:
        photo_dict = {}
        photo_dict['author'] = story.author.first_name + ' ' + story.author.last_name
        photo_dict['username'] = story.author.username
        photo_dict['avatar'] = str(story.author.avatar)
        photo_dict['story_id'] = story.id
        photo_dict['title'] = story.title
        photo_dict['photo'] = str(story.photo)
        photo_dict['country'] = story.country
        photo_dict['category'] = story.category
        page_of_photos.append(photo_dict)
    print(page_of_photos)

    # 封装一下数据
    data = {
        # 注意这里得到的当前页码的数据列表是QuerySet，不能直接返回前端，会报错
        # 还需要拿到data后简单转换一下
        # 'objects_list': page_of_obj,
        'photos_in_list': page_of_photos,
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
