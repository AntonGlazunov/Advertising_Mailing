from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('blog_list', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('blog/<int:pk>', cache_page(60)(BlogDetailView.as_view()), name='blog_detail'),
    path('create', BlogCreateView.as_view(), name='add_blog'),
    path('edit/<int:pk>', BlogUpdateView.as_view(), name='update_blog'),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name='delete'),
]
