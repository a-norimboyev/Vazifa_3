from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("post/create/", views.post_create_view, name="post_create"),
    path("post/<slug:slug>/", views.post_detail_view, name="post_detail"),
    path("my-posts/", views.my_posts_view, name="my_posts"),
    path("category/<slug:slug>/", views.category_posts_view, name="category_posts"),
    path("tag/<slug:slug>/", views.tag_posts_view, name="tag_posts"),
]

