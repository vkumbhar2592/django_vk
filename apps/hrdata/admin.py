from django.contrib import admin

# Register your models here. 

from .models import Topic, Tag, Document, Region



admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(Document)
admin.site.register(Region)
