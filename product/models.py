from django.db import models


class Products(models.Model):
    image = models.ImageField(upload_to='image/', default='image/Untitled1.jpg')
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    inventory = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Create your models here.
