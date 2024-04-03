# from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"This is question number {i}"
    } for i in range(100)
]

ANSWERS = [
    [
        {
            "id": i,
            "title": f"Answer {i}",
            "text": f"This is answer number {j} on question {i}"
        } for j in range(3)
    ] for i in range(100)
]

BEST_MEMBERS = [
    'Mr. Freeman', 'Dr. House', 'Bender', 'Queen Victoria', 'V. Pupkin'
]

TAGS = [
    'perl', 'python', 'TechnoPark', 'MySQL', 'django', 'Mail.Ru', 'Voloshin', 'Firefox'
]


def func_paginator(page_num, items):
    paginator = Paginator(items, per_page=5)
    if not (type(page_num) is int) or not (1 <= int(page_num) <= paginator.num_pages):
        page_num = 1
    page_obj = paginator.page(page_num)
    return page_obj


def index(request):
    page_obj = func_paginator(request.GET.get('page', 1), QUESTIONS)
    return render(request, template_name="index.html",
                  context={"page_obj": page_obj, "best_members": BEST_MEMBERS, "tags": TAGS})
    # return HttpResponse("Hello, world")


def hot(request):
    questions = QUESTIONS[:5]
    page_obj = func_paginator(request.GET.get('page', 1), questions)
    return render(request, template_name="hot.html",
                  context={"page_obj": page_obj, "best_members": BEST_MEMBERS, "tags": TAGS})


def question(request, question_id):
    item_question = QUESTIONS[question_id]
    list_item_answers = ANSWERS[question_id]
    page_obj = func_paginator(request.GET.get('page', 1), list_item_answers)
    return render(request, template_name="question.html",
                  context={"page_obj": page_obj, "question": item_question, "answers": list_item_answers,
                           "best_members": BEST_MEMBERS,
                           "tags": TAGS})


def ask(request):
    return render(request, template_name="ask.html", context={"best_members": BEST_MEMBERS, "tags": TAGS})


def login(request):
    return render(request, template_name="login.html", context={"best_members": BEST_MEMBERS, "tags": TAGS})


def register(request):
    return render(request, template_name="register.html", context={"best_members": BEST_MEMBERS, "tags": TAGS})


def settings(request):
    return render(request, template_name="settings.html", context={"best_members": BEST_MEMBERS, "tags": TAGS})


def tag(request, tag_name):
    page_obj = func_paginator(request.GET.get('page', 1), QUESTIONS)
    return render(request, template_name="tag.html",
                  context={"tag": tag_name, "page_obj": page_obj, "best_members": BEST_MEMBERS, "tags": TAGS})


def member(request, member_name):
    return render(request, template_name="member.html",
                  context={"member": member_name, "best_members": BEST_MEMBERS, "tags": TAGS})
