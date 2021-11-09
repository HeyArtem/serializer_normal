from django.contrib import admin
from .models import BlogPost, BlogPostCategory, BlogPostTag

# не забыв импортнуть, я заргистировал мои модели
admin.site.register(BlogPost)
admin.site.register(BlogPostCategory)
admin.site.register(BlogPostTag)
