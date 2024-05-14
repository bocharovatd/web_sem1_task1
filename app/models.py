from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum


class ProfileManager(models.Manager):
    def get_top(self):
        return self.annotate(nanswers=Count('answer')).order_by('-nanswers')[:5]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = ProfileManager()


class QuestionManager(models.Manager):
    def get_current(self):
        return self.order_by('created_at').reverse()

    def get_hot(self):
        return self.annotate(nlikes=Count('questionlike')).order_by('-nlikes')


class Question(models.Model):
    title = models.TextField()
    text = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = QuestionManager()


class ScoreManager(models.Manager):
    def likes(self):
        return self.get_queryset().filter(type__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(type__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('type')).get('type__sum') or 0


class QuestionScore(models.Model):
    TYPE = {1: 'like', -1: 'dislike'}
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    type = models.IntegerField(choices=TYPE)
    objects = ScoreManager()

    class Meta:
        unique_together = ('user', 'question')


class Answer(models.Model):
    text = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class AnswerScore(models.Model):
    TYPE = {1: 'like', -1: 'dislike'}
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    type = models.IntegerField(choices=TYPE)
    objects = ScoreManager()

    class Meta:
        unique_together = ('user', 'answer')


class TagManager(models.Manager):
    def get_top(self):
        return self.annotate(nquestions=Count('questions')).order_by('-nquestions')[:8]


class Tag(models.Model):
    name = models.TextField()
    questions = models.ManyToManyField(Question)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = TagManager()
