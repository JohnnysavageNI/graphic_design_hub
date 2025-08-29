from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path(
        "request/<int:pk>/edit/",
        views.request_edit,
        name="request_edit",
    ),
    path(
        "request/<int:pk>/delete/",
        views.request_delete,
        name="request_delete",
    ),
]
