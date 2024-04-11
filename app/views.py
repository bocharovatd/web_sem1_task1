# from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render
from app.models import *


def func_paginator(page_num, items):
    paginator = Paginator(items, per_page=5)
    try:
        page_obj = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page_obj = paginator.page(1)
    return page_obj


def index(request, user=None):
    current_questions = Question.objects.get_current()
    print(request.GET.get('page'))
    page_obj = func_paginator(request.GET.get('page', 1), current_questions)
    return render(request, template_name="index.html",
                  context={"page_obj": page_obj,
                           "best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "user": user})
    # return HttpResponse("Hello, world")


def hot(request, user=None):
    hot_questions = list(Question.objects.get_hot())
    page_obj = func_paginator(request.GET.get('page', 1), hot_questions)
    return render(request, template_name="hot.html",
                  context={"page_obj": page_obj,
                           "best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "user": user})


def question(request, question_id, user=None):
    item_question = Question.objects.get(id=question_id)
    list_item_answers = list(Answer.objects.filter(question=item_question).order_by('created_at').reverse())
    page_obj = func_paginator(request.GET.get('page', 1), list_item_answers)
    return render(request, template_name="question.html",
                  context={"page_obj": page_obj,
                           "question": item_question,
                           "best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "user": user})


def ask(request, user=None):
    return render(request, template_name="ask.html",
                  context={"best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "user": user})


def login(request):
    user = None
    return render(request, template_name="login.html",
                  context={"best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "user": user})


def register(request):
    user = None
    return render(request, template_name="register.html",
                  context={"best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "user": user})


def settings(request, user=None):
    return render(request, template_name="settings.html",
                  context={"best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "user": user})


def tag(request, tag_name, user=None):
    tag_questions = list(Tag.objects.get(name=tag_name).questions.get_current())
    page_obj = func_paginator(request.GET.get('page', 1), tag_questions)
    return render(request, template_name="tag.html",
                  context={"tag": tag_name,
                           "page_obj": page_obj,
                           "best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "user": user})


def member(request, member_name, user=None):
    return render(request, template_name="member.html",
                  context={"member": member_name,
                           "best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "user": user})


def error_404_view(request, exception):
    return render(request, '404.html')
