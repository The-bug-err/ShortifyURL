from django.db import models

# Create your models here.


class UrlMap(models.Model):
    short_url = models.CharField(max_length=200)
    original_url = models.CharField(max_length=200)

    def __str__(self):
        return '{} is short URL for {}'.format(self.short_url, self.original_url)
