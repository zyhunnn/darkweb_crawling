from .models import *
from rest_framework import generics
from rest_framework.response import Response
from .serializers import URLSerializer, wordSerializer
from rest_framework.permissions import AllowAny
from urllib.parse import urlparse


class url_List(generics.ListCreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset=URL.objects.all()
        return queryset
    
    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        parameters = parsed_url.query
        title = request.data.get('title')

        existing_url = URL.objects.filter(url=url).first()

        if existing_url:
            existing_url.save()
            serializer = self.get_serializer(existing_url)
            return Response(serializer.data)

        new_url = URL.objects.create(url=url, domain=domain, parameters=parameters, title=title)
        serializer = self.get_serializer(new_url)
        return Response(serializer.data)

class Word_List(generics.ListCreateAPIView):
    queryset = word_count.objects.all()
    serializer_class = wordSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.kwargs.get('url_id'):
            return word_count.objects.filter(url=self.kwargs.get('url_id'))
        return word_count.objects.all()
    
    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        word = request.data.get('word')
        count = request.data.get('count')

        existing_word = word_count.objects.filter(url=url, word=word).first()

        if existing_word:
            existing_word.count = count
            existing_word.save()
            serializer = self.get_serializer(existing_word)
            return Response(serializer.data)

        return super().create(request, *args, **kwargs)