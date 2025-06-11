from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.products, name='products'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('categories/', views.categories, name='categories'),
    path('stockin/', views.stock_in, name='stockin'),
    path('stockout/', views.stock_out, name='stockout'),
    path('logout/', views.logout_view, name='logout'),
    

]
