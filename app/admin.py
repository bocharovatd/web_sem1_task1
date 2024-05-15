from django.contrib import admin

from app import models

admin.site.register(models.Profile)
admin.site.register(models.Question)
admin.site.register(models.QuestionScore)
admin.site.register(models.Answer)
admin.site.register(models.AnswerScore)
admin.site.register(models.Tag)

# Register your models here.
