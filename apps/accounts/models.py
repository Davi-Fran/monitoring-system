from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    photo = models.ImageField(upload_to="users/photos/", blank=True)

    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        db_table = "app_user"