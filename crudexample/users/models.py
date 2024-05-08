# models.py

from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True, max_length=20)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    emailId = models.EmailField(max_length=50)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def check_password(self, raw_password):
        # Check if the provided password matches the hashed password
        return check_password(raw_password, self.password)
