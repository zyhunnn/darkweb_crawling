from django.urls import path
from .views import *

urlpatterns = [
    path('api/urllist/', url_List.as_view()),
    path('api/wordlist/', Word_List.as_view()),
    path('api/wordlist/<int:url_id>/', Word_List.as_view())
]