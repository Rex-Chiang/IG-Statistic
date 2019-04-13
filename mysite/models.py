from django.db import models
from django.utils import timezone

# Create your models here.
class Article(models.Model):
    account = models.CharField(max_length = 20)
    followers = models.IntegerField(default = 0)
    following = models.IntegerField(default = 0)
    articles = models.IntegerField(default = 0)
    Most_Liked_Posts = models.IntegerField(default = 0)
    Most_Commented_Posts = models.IntegerField(default = 0)
    Least_Liked_Posts = models.IntegerField(default = 0)
    Least_Commented_Posts = models.IntegerField(default = 0)
    pub_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.account

class PicInfo(models.Model):
    account = models.CharField(max_length = 20)
    pic = models.URLField(max_length = 300)
    like = models.IntegerField(default = 0)
    comment = models.IntegerField(default = 0)

    def __str__(self):
        return self.account
