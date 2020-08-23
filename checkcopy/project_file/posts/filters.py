import django_filters
from .models import postspage

class order_filter(django_filters.FilterSet):
    class Meta:
        model = postspage
        fields=['user','category','content']
