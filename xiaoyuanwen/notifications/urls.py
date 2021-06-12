from django.urls import path

from xiaoyuanwen.notifications import views


app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationUnreadListView.as_view(), name="unread"),
    path('latest-notifications/', views.get_latest_notifications, name="latest_notifications"),
    path('mark-as-read/<str:slug>/', views.mark_as_read, name="mark_as_read"),
    path('mark-all-read/', views.mark_all_as_read, name="mark_all_read"),
]
