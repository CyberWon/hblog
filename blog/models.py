from django.db import models

# Create your models here.
class List(models.Model):
    # id = models.AutoField(max_length=10)
    title = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    keyword = models.CharField(max_length=20)
    description = models.TextField()
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)