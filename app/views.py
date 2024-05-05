# from django.http import HttpResponse
from django.contrib import auth, messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from app.forms import *
from app.models import *


def func_paginator(page_num, items):
    paginator = Paginator(items, per_page=5)
    try:
        page_obj = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page_obj = paginator.page(1)
    return page_obj


def index(request):
    current_questions = Question.objects.get_current()
    page_obj = func_paginator(request.GET.get('page', 1), current_questions)
    return render(request, template_name="index.html",
                  context={"page_obj": page_obj,
                           "best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top()})


def hot(request):
    hot_questions = list(Question.objects.get_hot())
    page_obj = func_paginator(request.GET.get('page', 1), hot_questions)
    return render(request, template_name="hot.html",
                  context={"page_obj": page_obj,
                           "best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top()})


@require_http_methods(['GET', 'POST'])
def question(request, question_id):
    item_question = Question.objects.get(id=question_id)
    list_item_answers = list(Answer.objects.filter(question=item_question).order_by('created_at')[::-1])
    if request.method == 'POST':
        if request.user.is_authenticated:
            answer_form = AnswerForm(request.user, item_question, request.POST)
            if answer_form.is_valid():
                answer_id = answer_form.save()
                return redirect(f"{reverse('question', args=(question_id,))}?#{answer_id}")
        else:
            return redirect(f"{reverse('login')}?continue={request.path}")
    else:
        answer_form = AnswerForm(request.user, item_question)
    page_obj = func_paginator(request.GET.get('page', 1), list_item_answers)
    return render(request, template_name="question.html",
                  context={"page_obj": page_obj,
                           "question": item_question,
                           "best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "form": answer_form})


@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
def ask(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.user, request.POST)
        if question_form.is_valid():
            question_id = question_form.save()
            return redirect(reverse('question', args=(question_id,)))
        else:
            if question_form.non_field_errors():
                messages.error(request, *question_form.non_field_errors())
    else:
        question_form = QuestionForm(request.user)
    return render(request, template_name="ask.html",
                  context={"best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "form": question_form})


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.GET.get('continue', reverse('index')))
            else:
                messages.error(request, "Authentication failed")
    else:
        login_form = LoginForm()
    return render(request, template_name="login.html",
                  context={"best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "form": login_form})


@login_required(login_url='login', redirect_field_name='continue')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            auth.login(request, user)
            return redirect(reverse('index'))
        else:
            if signup_form.non_field_errors():
                messages.error(request, *signup_form.non_field_errors())
    else:
        signup_form = SignupForm()
    return render(request, template_name="signup.html",
                  context={"best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "form": signup_form})


@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
def settings(request):
    if request.method == 'POST':
        settings_form = SettingsForm(request.POST, request.FILES,
                                     instance=request.user)
        if settings_form.is_valid():
            user = settings_form.save()
            auth.login(request, user)
            return redirect(reverse('settings'))
        else:
            if settings_form.non_field_errors():
                messages.error(request, *settings_form.non_field_errors())
    else:
        settings_form = SettingsForm(instance=request.user, initial={'avatar': request.user.profile.avatar})
    return render(request, template_name="settings.html",
                  context={"best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top(),
                           "form": settings_form})


def tag(request, tag_name):
    tag_questions = list(Tag.objects.get(name=tag_name).questions.get_current())
    page_obj = func_paginator(request.GET.get('page', 1), tag_questions)
    return render(request, template_name="tag.html",
                  context={"tag": tag_name,
                           "page_obj": page_obj,
                           "best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top()})


def member(request, member_name):
    return render(request, template_name="member.html",
                  context={"member": member_name,
                           "best_members": Profile.objects.get_top(),
                           "popular_tags": Tag.objects.get_top()})


def error_404_view(request, exception):
    return render(request, '404.html')
