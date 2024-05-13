from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ['id', 'keyword', 'url', 'domain', 'parameters', 'title', 'prev_url', 'createdAt', 'updatedAt']

class wordSerializer(serializers.ModelSerializer):
    class Meta:
        model = word_count
        fields = ['id', 'keyword', 'url', 'word', 'count', 'createdAt', 'updatedAt']