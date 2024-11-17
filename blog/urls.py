from django.urls import path
from .views import BlogView, BlogDetailView, EditPostView, DeletePostView, CategoryView, LikeView, VisitView, add_post, search_blog, category_view

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('article/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('add_post/', add_post, name='add_post'),
    path('edit_post/<int:pk>/', EditPostView.as_view(), name='edit_post'),
    path('article/<int:pk>/remove/', DeletePostView.as_view(), name='delete_post'),
    path('blog_category/<str:cat>/', category_view, name='blog_category'),
    path('like/<int:pk>/', LikeView, name='like_post'),
    path('post/<int:pk>/', VisitView, name='visit_post'),
    path('search_blog/', search_blog, name='search_blog'),
]

