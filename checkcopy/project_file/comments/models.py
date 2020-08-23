from django.db import models
# from posts.models import postspage
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class CommentManager(models.Manager):

    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id= obj_id).filter(parent=None)
        return qs


class Comment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE,default=1)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,default=None)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    parent      = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    content     = models.TextField(max_length=300)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects=CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.user.username)

    def children(self): #replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True