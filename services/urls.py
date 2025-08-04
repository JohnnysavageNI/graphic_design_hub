from django.urls import path
from . import views


urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('checkout/<int:service_id>/', views.create_checkout_session, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
