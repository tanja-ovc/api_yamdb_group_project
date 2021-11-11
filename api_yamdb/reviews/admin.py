from django.contrib import admin

from .models import Category, Comment, Genre, Genre_Title, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class Genre_TitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'title', 'score', 'pub_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'review', 'pub_date')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Genre_Title, Genre_TitleAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
