from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount, Comment, EventPost,AttendingEvent, RvspEvent

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Comment)
admin.site.register(EventPost)
admin.site.register(AttendingEvent)
admin.site.register(RvspEvent)
