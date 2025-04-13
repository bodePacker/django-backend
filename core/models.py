from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, primary_key=True)
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    
    def __str__(self):
        return self.username

class KeyboardMapping(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='mappings')
    mappings = models.JSONField()
    name = models.CharField(max_length=50, default='Unamed Mapping')
    description = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        mapping_name = self.mappings.get('name', 'Unnamed Mapping')
        status = '(Active)' if self.is_active else ''
        return f"{self.user.username}'s {mapping_name} {status}"

    class Meta:
        ordering = ['-updated_at']  # Most recent mappings first