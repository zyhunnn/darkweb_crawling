from django.shortcuts import render
from .models import *
from rest_framework import generics
from rest_framework.response import Response
from .serializers import URLSerializer, wordSerializer
from rest_framework.permissions import AllowAny


class url_List(generics.ListCreateAPIView):
    queryset = URL_Crawler.objects.all()
    serializer_class = URLSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset=URL_Crawler.objects.all()
        return queryset

class Word_List(generics.ListCreateAPIView):
    queryset = word_count.objects.all()
    serializer_class = wordSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.kwargs.get('url_id'):
            return word_count.objects.filter(url=self.kwargs.get('url_id'))
        return word_count.objects.all()

    def post(self, request):
        url_crawler_instance = URL_Crawler.objects.get(id=1)
        word_count.objects.create(url=url_crawler_instance,word=1,count=1)
        return Response("success")
    