from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:question_id>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('member/<str:member_name>/', views.member, name='member'),
]

handler404 = 'app.views.error_404_view'
