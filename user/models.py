from django.db import models
from django.contrib.auth.hashers import make_password


class UserModel(models.Model):
    class Meta:
        db_table = 'user'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.password = make_password(password=self.password)
        super().save(*args, **kwargs)
