# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tweet(models.Model):
    tweet_handle = models.CharField(max_length=100)
    tweet_id = models.BigIntegerField(unique=True)
    tweet_date = models.DateTimeField()
    tweet_location_x = models.DecimalField(null=True, max_digits=18,decimal_places=15)
    tweet_location_y = models.DecimalField(null=True, max_digits=18,decimal_places=15)

    def __str__(self):
        return self.tweet_location

