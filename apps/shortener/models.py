from hashlib import md5
from django.db import models


class Shortener(models.Model):
    main_url = models.URLField(unique=True)
    shortened_url = models.CharField(max_length=30, unique=True, null=True, blank=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.clicks += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.shortened_url:
            self.shortened_url = md5(self.main_url.encode()).hexdigest()[:5]

        return super().save(*args, **kwargs)
