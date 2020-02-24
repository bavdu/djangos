from django.urls import path
from . import views


urlpatterns = [
    path('', views.response, name='response'),
    path('<str:questions_id>/', views.detail, name='detail'),
    path('<str:questions_id>/result/', views.results, name='result'),
    path('<str:questions_id>/votes/', views.votes, name='votes')
]
