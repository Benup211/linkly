import random
import string
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_short_code():
    length = random.randint(4, 8)
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class Link(models.Model):
    short_code = models.CharField(max_length=8, unique=True, primary_key=True, editable=False)
    original_url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hits = models.PositiveIntegerField(default=0)
    user = models.ManyToManyField(User,blank=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            while True:
                short_code = generate_short_code()
                if not Link.objects.filter(short_code=short_code).exists():
                    self.short_code = short_code
                    break
        super().save(*args, **kwargs)