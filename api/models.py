from django.db import models

class URL(models.Model):
    url = models.TextField()
    domain = models.TextField()
    parameters = models.TextField()
    title = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-createdAt']

class word_count(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE) 
    word = models.TextField()
    count = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-createdAt']