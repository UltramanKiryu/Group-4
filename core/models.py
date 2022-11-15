from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
import uuid
import datetime

# Create your models here.
User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birthday = models.DateField(_("Date"), default=datetime.date.today)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile_picture.png')
    location = models.CharField(max_length=100, blank=True)

    def _str_(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    id_str = models.CharField(max_length=500, default="")
    user = models.CharField(max_length=50)
    o_user = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(max_length=50)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    no_of_likes = models.IntegerField(default=0)


    def _str_(self):
        return self.user

class Comment(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    text = models.TextField(max_length=50)

    def _str_(self):
        return self.username

class LikePost(models.Model):
    post_id=models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def _str_(self):
        return self.username
        
class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    re = models.IntegerField(default=0)
    user = models.CharField(max_length=100)

    def _str_(self):
        return self.user

