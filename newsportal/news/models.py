from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum



class Author (models.Model):
    user = models.OneToOneField (User, on_delete = models.CASCADE)
    rating = models.IntegerField (default = 0)

    def update_rating(self):
        articles_rate = Post.objects.filter (one_to_many_relation=self.pk).aggregate (Sum('post_rating')) ['post_rating__sum'] * 3
        comments_rate = Comment.objects.filter (users_id=self.users).aggregate (sum_articles=Sum ('comment_rate')) ['comment_rate']
        comments_articles_rate = Comment.objects.filter (post__author__users=self.users).aggregate (sum_posts=Sum ('comment_rate')) ['comment_rate']
        self.rating = articles_rate + comments_rate + comments_articles_rate
        self.save ()


class Category (models.Model):
    name = models.CharField (max_length = 255,
                             unique = True)


class Post (models.Model):
    articles = 'AR'
    news = 'NE'
    TYPES = [
        (news, 'Новости'),
        (articles, 'Статьи')
    ]

    author = models.ForeignKey (Author, on_delete = models.CASCADE)
    choice_types = models.CharField (max_length=2, choices=TYPES, default=news)
    time_in = models.DateTimeField (auto_now_add = True)
    categories = models.ManyToManyField (Category, through='PostCategory')
    news_title = models.CharField (max_length=255)
    news_text = models.TextField ()
    news_rating = models.IntegerField (default=0)

    def like (self):
        self.post_rating += 1
        self.save ()

    def dislike (self):
        self.post_rating -= 1
        self.save ()

    def preview (self):
        if len (self.content) > 124:
            return self.content [:124] + '...'
        else:
            return self.content


class PostCategory (models.Model):
    post = models.ForeignKey (Post, on_delete=models.CASCADE)
    category = models.ForeignKey (Category, on_delete=models.CASCADE)


class Comment (models.Model):
    post = models.ForeignKey (Post, on_delete = models.CASCADE)
    user = models.ForeignKey (User, on_delete=models.CASCADE)
    comment_text = models.TextField ()
    time_in_comment = models.DateTimeField (auto_now_add=True)
    comment_rating = models.IntegerField (default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()