from django.contrib import admin

from .models import postspage

class PostModelAdmin(admin.ModelAdmin):
    list_display= ["timestamp","category","update"]
    list_filter=["timestamp","category","user"]
    search_fields=["category","user","content"]
    class Meta:
        model=postspage


admin.site.register(postspage,PostModelAdmin)