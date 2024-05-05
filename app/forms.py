from django import forms
from app.models import Profile, Question, Tag, Answer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'dr_pepper'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))


class SignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'dr_pepper'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'sr_pepper@mail.ru'}))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    repeat_password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists')
        return email

    def clean(self):
        super().clean()
        if self.cleaned_data.get('password') != self.cleaned_data.get('repeat_password'):
            raise ValidationError('Passwords do not match')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        data = self.cleaned_data
        user.set_password(data['password'])
        profile = Profile(user=user)
        avatar = data['avatar']
        if avatar:
            profile.avatar = avatar
        if commit:
            user.save()
            profile.save()
        return user


class SettingsForm(forms.ModelForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'dr_pepper'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'placeholder': 'sr_pepper@mail.ru'}))
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        data = self.cleaned_data
        avatar = data['avatar']
        if avatar:
            user.profile.avatar = avatar
        if commit:
            user.save()
            user.profile.save()
        return user


class QuestionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'rows': 1}))
    text = forms.CharField(widget=forms.TextInput(attrs={'rows': 8}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'rows': 1}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Question
        fields = ['title', 'text']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tags = " ".join(map(lambda word: "".join(symb for symb in word if symb.isalpha()), tags.split()))
        return tags

    def save(self, commit=True):
        data = self.cleaned_data
        question = Question(title=data['title'], text=data['text'], user=self.user.profile)
        if commit:
            question.save()
            for tag in data['tags'].split():
                tag_object, created = Tag.objects.get_or_create(name=tag)
                tag_object.questions.add(question)
                tag_object.save()
        return question.id


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your answer here...', 'rows': 4}))

    def __init__(self, user, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.question = question

    class Meta:
        model = Answer
        fields = ['text']

    def save(self, commit=True):
        data = self.cleaned_data
        answer = Answer(text=data['text'], user=self.user.profile, question=self.question)
        if commit:
            answer.save()
        return answer.id
