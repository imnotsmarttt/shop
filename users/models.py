from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    slug = models.SlugField(db_index=True)

    class Meta:
        db_table = 'CustomUser'

    def save(self, *args, **kwargs):
        self.slug = self.username
        return super().save()
