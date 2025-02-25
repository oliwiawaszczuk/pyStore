from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique = True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username