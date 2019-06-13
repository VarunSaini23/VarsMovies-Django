from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


# Create your models here.
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    comment_text = models.CharField(max_length=1024)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_on = models.DateTimeField(default=now)
    movie_id = models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text
