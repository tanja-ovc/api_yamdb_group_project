from django.contrib import admin

from .models import Category, Comment, Genre, Genre_Title, Review, Title

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Genre_Title)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
