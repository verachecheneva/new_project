from django.db import models

from users.models import User
from .validators import validate_year, validate_score


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)


class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(validators=[validate_year], db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='category_titles', null=True)
    genre = models.ManyToManyField(Genre, related_name='genre_titles',
                                   blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('year',)


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='title_review')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(validators=[validate_score])
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_comment')
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    text = models.TextField(verbose_name='comment text')

    class Meta:
        ordering = ('pub_date',)
