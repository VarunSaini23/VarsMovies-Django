from django.contrib import admin

# Register your models here.
from movies.models import Collection, Comment

admin.site.register(Collection)
admin.site.register(Comment)
