from __future__ import unicode_literals
from django.db import models
from django.conf import settings 
from django.urls import reverse
from PIL import Image
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType


class postspage(models.Model):
    content=models.CharField(max_length=100,blank=True,null=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,models.CASCADE, default=1)
    category =models.CharField(blank=True,null=True,max_length=30)
    timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
    update=models.DateTimeField(auto_now=True,auto_now_add=False)
    image=models.FileField(blank=True)

    def __str__(self):
        return str(self.category)

    def get_absolute_url(self):
        return "/%s" %(self.id)


    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.path) # Open image using self

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image.path)