from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserModel(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

    def __str__(self):
        return self.username


class CategoryModel(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PostModel(models.Model):
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    overview = models.TextField()
    content = RichTextUploadingField('Content')
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails', null=True, blank=True)
    view_count = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.title

    @property
    def get_view_count(self):
        return PostView.objects.filter(post=self).count()


class Newsletter(models.Model):
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.email


class Comments(models.Model):
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post} - {self.author}'


class PostView(models.Model):
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username

