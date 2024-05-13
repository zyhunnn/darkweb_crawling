from django.db import models

class URL(models.Model):
    keyword = models.TextField()
    url = models.TextField()
    domain = models.TextField()
    parameters = models.TextField()
    title = models.TextField()
    prev_url = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-createdAt']

class word_count(models.Model):
    keyword = models.TextField()
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    word = models.TextField()
    count = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-createdAt']