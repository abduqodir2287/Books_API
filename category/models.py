from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400)

    def __str__(self) -> str:
        return f"Category name: {self.name}"
