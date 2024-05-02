from django.urls import path
from .views import *

urlpatterns = [
    path('api/url/', url_List.as_view()),
    path('api/word/', Word_List.as_view()),
    path('api/word/<int:url_id>/', Word_List.as_view())
]