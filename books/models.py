from django.db import models

from category.models import Category


class Books(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=55)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    description = models.CharField(max_length=1000, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

