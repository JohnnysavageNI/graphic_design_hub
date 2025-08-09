from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<int:service_id>/', views.add_to_cart, name='add_to_cart'),
    path('mini/', views.mini_cart_fragment, name='mini_cart_fragment'),
    path('remove/<int:service_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrement/<int:service_id>/', views.decrement_from_cart, name='decrement_from_cart'),
]
