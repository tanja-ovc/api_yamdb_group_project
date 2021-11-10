from django.contrib import admin

from .models import Comments, Review

admin.site.register(Review)
admin.site.register(Comments)
