from django.db import models
from .middleware import get_current_user
import random

# Create your models here.
def generate_random_id():
    # Generate a random integer within a range
    # Adjust the range according to your needs
    return str(random.randint(1540, 999999999999999999999999999999))


class ChatLog(models.Model):
    id = models.TextField(primary_key=True, default=generate_random_id, editable=False)
    question = models.TextField()
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    comment = models.TextField(default='')
    prompt = models.TextField()
    is_bookmarked = models.BooleanField(default=False)
    response = models.TextField()
    model_name = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    last_updated_by = models.CharField(max_length=100, default='')
    def save(self, *args, **kwargs):
        current_user = get_current_user()
        if current_user and not current_user.is_anonymous:
            self.last_updated_by = current_user.email
        super().save(*args, **kwargs)
    # Add other fields for chat logs here

    def __str__(self):
        return f"ChatLog - prompt: {self.prompt}"
