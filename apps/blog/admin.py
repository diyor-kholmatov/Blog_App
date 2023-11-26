from django.contrib import admin
from apps.blog.models import BlobCategory, Content
admin.site.register(Content)
admin.site.register(BlobCategory)
