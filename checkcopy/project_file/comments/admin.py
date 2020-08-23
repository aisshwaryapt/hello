from django.contrib import admin

# Register your models here.
from .models import Comment


class PostModelAdmin(admin.ModelAdmin):
    list_display= ["timestamp"]
    list_filter=["timestamp","user"]
    search_fields=["user","content_type"]
    class Meta:
        model=Comment


admin.site.register(Comment,PostModelAdmin) 
