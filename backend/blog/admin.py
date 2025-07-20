from django.contrib import admin
from .models import User, Category, Tag, Post, Comment, Subscription, PostLike, ForbiddenWord

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Subscription)
admin.site.register(PostLike)
admin.site.register(ForbiddenWord)
