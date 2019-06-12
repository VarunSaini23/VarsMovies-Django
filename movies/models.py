from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Collection(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie_id = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
