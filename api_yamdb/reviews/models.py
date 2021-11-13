from django.db import models
from django.db.models.constraints import UniqueConstraint

from users.models import MyUser as User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        blank=True, null=True, db_constraint=False)

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='genres',
        db_constraint=False
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='titles',
        db_constraint=False
    )

    def __str__(self):
        return f'Отношение {self.title} к жанру {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        db_constraint=False
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        db_constraint=False
    )
    score = models.PositiveSmallIntegerField(
        choices=[(n, str(n)) for n in range(1, 11)],
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('author', 'title',), name='unique_review'
            ),
        )

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        db_constraint=False
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        db_constraint=False
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text
