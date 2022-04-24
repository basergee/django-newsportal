from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    article = 'AR'
    news = 'NE'
    post_types = [(article, 'статья'), (news, 'новость')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(
        max_length=2,
        choices=post_types,
        default=article
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.TextField()
    content = models.TextField()
    rank = models.IntegerField(default=0)

    def like(self):
        self.rank += 1
        self.save()

    def dislike(self):
        if self.rank > 0:
            self.rank -= 1
            self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    rank = models.IntegerField(default=0)

    def like(self):
        self.rank += 1
        self.save()

    def dislike(self):
        if self.rank > 0:
            self.rank -= 1
            self.save()
