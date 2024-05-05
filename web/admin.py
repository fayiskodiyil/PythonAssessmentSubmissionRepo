from django.contrib import admin

from .models import Repository, Topic

admin.site.register(Repository)
admin.site.register(Topic)
