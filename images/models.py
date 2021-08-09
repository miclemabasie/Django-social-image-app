from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    url = models.URLField()
    image = models.ImageField(upload_to='%Y/%m/%d')
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=250)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    users_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    def __str_(self):
        return self.title

    def get_absolute_url(self):
        return reverse('images:image-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
