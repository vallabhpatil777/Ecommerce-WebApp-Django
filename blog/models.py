from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField


class Category(models.Model):
    """ Category model Design """
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    name = models.CharField(max_length=255)
    
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog')
    


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    snippet = models.CharField(max_length=255)
    body = RichTextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name='blog_posts', blank=True, null=True)
    visit = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads/blog/posts/', default='shop/media/uploads/products/GettyImages-912168376-fb70bef6e7db4af59a02f5b0f69b9366_eAeD77X.webp')
    
    
    def total_likes(self):
        return self.like.count()
    
    def total_visits(self):
        return self.visit.count()
    
    
    def __str__(self) -> str:
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('blog')
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    
    def __str__(self) -> str:
        return f'{self.user.username} comment on {self.post.title}'
    
    
