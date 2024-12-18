from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    slug = models.SlugField(unique=True, max_length=150, editable=False)
    # title = Aydın Gezimizden Merhaba
    # slug = aydin-gezimizden-merhaba
    # title = Bugün Aspendos Tarihi Mekanını Geziyoruz
    # slug = bugun-aspendos-tarihi-mekanini-geziyoruz
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    related_name='modified_by')

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def get_slug(self):
        slug = slugify(self.title.replace("ı", "i"))
        # title = Aydın Gezimizden Merhaba
        # slug = aydin-gezimizden-merhaba
        # title = Aydın Gezimizden Merhaba
        # slug = aydin-gezimizden-merhaba
        unique = slug
        number = 1
        while Post.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            # slug = aydin-gezimizden-merhaba
            # unique = aydin-gezimizden-merhaba-3
            number += 1

        return unique

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        self.slug = self.get_slug()
        return super(Post, self).save(*args, **kwargs)
