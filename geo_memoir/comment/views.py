import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext as _

from comment.models import Comment
from story.models import Story
from utils.get_lang import get_lang_code, translate
from utils.logging_check import *


# error code  10500-10599   used 10500-10505
# Create your views here.
class CommentViews(View):

    def get(self, request, lang_code):
        # get current language
        cur_language = get_lang_code(request)
        login_user = get_user_by_request(request)

        story_id = request.GET.get('story_num', 0)
        try:
            story = Story.objects.get(id=story_id)
        except Exception as e:
            message = _('Story does not exist.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10500, 'msg': t_message})

        all_comments = Comment.objects.filter(story=story).order_by('-created_time')
        comments_list = []
        replies_dict = {}  # {1:[{rep},{rep}], 2:[{rep}],{rep}], 3:[{rep},{rep},{rep}], ...}
        for cmt in all_comments:
            if cmt.parent_comment:
                replies_dict.setdefault(cmt.parent_comment, [])
                replies_dict[cmt.parent_comment].append({
                    'r_id': cmt.id,
                    'commenter_avatar': str(cmt.commenter.avatar),
                    'commenter': cmt.commenter.first_name + ' ' + cmt.commenter.last_name,
                    'commenter_uname': cmt.commenter.username,
                    'content': cmt.content,
                    'created_time': cmt.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                })
            else:
                comments_list.append({
                    'id': cmt.id,
                    'commenter_avatar': str(cmt.commenter.avatar),
                    'commenter': cmt.commenter.first_name + ' ' + cmt.commenter.last_name,
                    'commenter_uname': cmt.commenter.username,
                    'content': cmt.content,
                    'created_time': cmt.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'replies_list': [],
                })

        # after seperating all cmts, match each cmt with its replies
        for c in comments_list:
            if c['id'] in replies_dict:
                c['replies_list'] = replies_dict[c['id']]

        # if user logs in --> return user
        user = None
        if login_user:
            user = {'username': login_user.username, 'avatar': str(login_user.avatar)}
        comments_list = comments_list
        comments_total = get_comments_length(comments_list)

        return JsonResponse({'code': 200, 'user': user, 'comments_total': comments_total, 'data': comments_list})

    @method_decorator(logging_check)
    def post(self, request, lang_code):
        cur_language = get_lang_code(request)
        user = request.login_user
        message = json.loads(request.body)
        story_id = message['story_id']
        content = message['content']
        parent_cmt_id = message['parent_cmt_id']

        try:
            story = Story.objects.get(id=story_id)
        except Exception as e:
            message = _('Story does not exist.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10501, 'msg': t_message})

        Comment.objects.create(content=content, parent_comment=parent_cmt_id, commenter=user, story=story)
        return JsonResponse({'code': 200})

    @method_decorator(logging_check)
    def put(self, request, lang_code):
        cur_language = get_lang_code(request)
        edited_comment = json.loads(request.body)
        cmt_id = edited_comment['cmt_id']
        content = edited_comment['content']
        if cmt_id:
            try:
                comment = Comment.objects.get(id=cmt_id)
            except Exception as e:
                message = _('Comment to be deleted does not exist.')
                t_message = translate(cur_language, message)
                return JsonResponse({'code': 10502, 'msg': t_message})
            comment.content = content
            comment.save()
            return JsonResponse({'code': 200})

        else:
            message = _('Comment to be deleted is not specified.')
            t_message = translate(cur_language, message)
            return JsonResponse({'code': 10503, 'msg': t_message})

    @method_decorator(logging_check)
    def delete(self, request, lang_code):
        cur_language = get_lang_code(request)
        comment_id = request.GET.get('cmt_num', 0)
        if comment_id:
            try:
                comment = Comment.objects.get(id=comment_id)
            except Exception as e:
                message = _('Comment to be deleted does not exist.')
                t_message = translate(message)
                return JsonResponse({'code': 10504, 'msg': t_message})
            comment.delete()
            return JsonResponse({'code': 200})

        else:
            message = _('Comment to be deleted is not specified.')
            t_message = translate(message)
            return JsonResponse({'code': 10505, 'msg': t_message})


def get_comments_length(comments_list):
    total = 0
    for r in comments_list:
        total_replies = len(r['replies_list'])
        total += (1 + total_replies)
    return total

