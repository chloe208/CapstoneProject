from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


class BillingProfile(models.Model):
    user = models.OneToOneField(User,unique =True, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
