from django.db import models
from .middleware import get_current_user  # Import the utility function

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Document(models.Model):
    tags = models.ManyToManyField(Tag)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE , default='')
    name = models.CharField(max_length=100)
    street_url = models.CharField(max_length=300)
    # content_html = models.TextField()
    content =  models.TextField()
    # content_LLM = models.TextField()
    last_updated_by = models.CharField(max_length=100, default='')
    
    
    def save(self, *args, **kwargs):
        current_user = get_current_user()
        if current_user and not current_user.is_anonymous:
            self.last_updated_by = current_user.email
        super().save(*args, **kwargs)

    last_updated = models.DateTimeField(auto_now=True) 
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return self.name