from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)

    def update_rating(self, rating: int):
        self.rank = rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return f'{self.name}'


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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

    def preview(self):
        return self.content[:124] + '...'

    def __str__(self):
        return f'{self.pk}'

    def get_absolute_url(self):
        return reverse('news_details', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}'


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

    def __str__(self):
        return f'{self.pk}'
