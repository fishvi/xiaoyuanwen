from test_plus.test import TestCase

from xiaoyuanwen.news.models import News
from xiaoyuanwen.notifications.models import Notification
from xiaoyuanwen.notifications.views import notification_handler


class TestNotificationsModels(TestCase):
    def setUp(self):
        self.user = self.make_user("testuser1")
        self.other_user = self.make_user("testuser2")
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
            verb="P"
        )

    def test_return_values(self):
        """测试对象类型和返回值"""
        assert isinstance(self.first_notification, Notification)
        assert isinstance(self.second_notification, Notification)
        assert isinstance(self.third_notification, Notification)
        assert str(self.first_notification) == "testuser1 赞了"
        assert str(self.second_notification) == "testuser1 评论了"
        assert str(self.third_notification) == "testuser2 回答了"

    def test_return_unread(self):
        """测试返回未读"""
        assert Notification.objects.unread().count() == 3
        assert self.first_notification in Notification.objects.unread()
        assert self.second_notification in Notification.objects.unread()
        assert self.third_notification in Notification.objects.unread()

    def test_mark_as_read_and_mark_as_unread(self):
        """测试标记为已读和标记为未读"""
        self.first_notification.mark_as_read()
        assert Notification.objects.read().count() == 1
        assert self.first_notification in Notification.objects.read()
        self.first_notification.mark_as_unread()
        assert Notification.objects.read().count() == 0

    def test_mark_all_as_read(self):
        """测试标记所有通知为已读"""
        Notification.objects.mark_all_as_read()
        assert Notification.objects.read().count() == 3
        Notification.objects.mark_all_as_unread(self.other_user)
        assert Notification.objects.read().count() == 1
        Notification.objects.mark_all_as_unread()
        assert Notification.objects.unread().count() == 3
        Notification.objects.mark_all_as_read(self.other_user)
        assert Notification.objects.read().count() == 2

    @staticmethod
    def test_get_most_recent():
        """测试获取最近的通知"""
        assert Notification.objects.get_most_recent().count() == 3

    def test_notification(self):
        """测试单个通知"""
        Notification.objects.mark_all_as_read()
        obj = News.objects.create(
            user=self.user,
            content="内容示例",
            reply=True
        )
        notification_handler(self.other_user, self.user, "C", obj)
        assert Notification.objects.unread().count() == 1
