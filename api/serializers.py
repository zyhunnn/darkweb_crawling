from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL_Crawler
        fields = ['id', 'URL', 'domain', 'parameters', 'title', 'createdAt', 'updatedAt']

class wordSerializer(serializers.ModelSerializer):
    class Meta:
        model = word_count
        fields = ['id', 'url', 'word', 'count', 'createdAt', 'updatedAt']