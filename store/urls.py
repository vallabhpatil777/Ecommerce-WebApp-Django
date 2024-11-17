from django.urls import path
from . import views

from .views import PasswordsChangeView, EditProfilePageView, CreateProfileView, ProductDetailView


urlpatterns = [
    path('', views.entrance, name='entrance'),
    path('main/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('category/<str:cat>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('user/edit_user/', views.UserEditView.as_view(), name='edit_user'),
    path('password/<int:pk>/', views.change_password, name='change_password'),
    
    path('<int:pk>/edit_profile/', views.EditProfilePageView.as_view(), name='edit_profile_page'),
    path('<int:pk>/profile/', views.profile_page_view, name='profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('search/', views.search_stuff, name='search_stuff'),
    path('payment/', views.payment, name='payment'),
    path('<int:pk>/admin_panel/', views.admin_panel, name='admin_panel'),
    path('pay/paypay', views.payment, name='paypay')
]
