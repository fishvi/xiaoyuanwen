from django.urls import path

from xiaoyuanwen.users import views

app_name = "users"

urlpatterns = [
    path("update/", views.UserUpdateView.as_view(), name="update"),
    path("<str:username>/", views.UserDetailView.as_view(), name="detail"),
]
