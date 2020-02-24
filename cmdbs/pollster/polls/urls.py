from django.urls import path
from . import views


urlpatterns = [
    path('<str:style>/', views.response, name='response'),
]
