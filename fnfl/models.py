from django.db import models
from django.utils import timezone

class Lineup(models.Model):
    author = models.ForeignKey('auth.User')
    week = models.CharField(max_length=50)
    qb = models.CharField(max_length=50)
    rb1 = models.CharField(max_length=50)
    rb2 = models.CharField(max_length=50)
    wr1 = models.CharField(max_length=50)
    wr2 = models.CharField(max_length=50)
    k = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.week