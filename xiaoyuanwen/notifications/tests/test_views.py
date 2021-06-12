from django.test import Client
from django.urls import reverse
from test_plus.test import TestCase

from xiaoyuanwen.notifications.models import Notification


class NotificationsViewsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("testuser1")
        self.other_user = self.make_user("testuser2")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="testuser1", password="password")
        self.other_client.login(username="testuser2", password="password")
        # testuser1赞了testuser2
        self.first_notification = Notification.objects.create(
            actor=self.user,
            recipient=self.other_user,
            verb="L"
        )
        # testuser1评论了testuser2
        self.second_notification = Notification.objects.create(
            actor=self.user,
            recipient=self.other_user,
            verb="C"
        )
        # testuser2回答了testuser1
        self.third_notification = Notification.objects.create(
            actor=self.other_user,
            recipient=self.user,
            verb="A"
        )

    def test_notification_unread_list(self):
        """测试testuser1未读通知列表"""
        response = self.client.get(reverse("notifications:unread"))
        assert response.status_code == 200
        assert self.third_notification in response.context["notification_list"]

    def test_mark_all_as_read(self):
        """测试testuser1收到的所有通知标为已读"""
        response = self.client.get(reverse("notifications:mark_all_read"), follow=True)
        assert '/notifications/' in str(response.context["request"])
        assert Notification.objects.unread().count() == 2

    def test_mark_as_read(self):
        """测试testuser1收到的某个通知标为已读，传递slug参数"""
        response = self.client.get(reverse("notifications:mark_as_read",
                                           kwargs={"slug": self.third_notification.slug}))
        assert response.status_code == 302
        assert Notification.objects.unread().count() == 2

    def test_latest_notifications(self):
        """测试testuser2最近收到的通知"""
        response = self.other_client.get(reverse("notifications:latest_notifications"))
        assert response.status_code == 200
        assert self.first_notification in response.context["notifications"]
        assert self.second_notification in response.context["notifications"]
