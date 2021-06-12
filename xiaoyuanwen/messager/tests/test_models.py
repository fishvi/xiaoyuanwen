from test_plus.test import TestCase

from xiaoyuanwen.messager.models import Message


class TestMessagesModels(TestCase):
    def setUp(self):
        self.user = self.make_user("testuser1")
        self.other_user = self.make_user("testuser2")
        self.first_message = Message.objects.create(
            sender=self.user,
            recipient=self.other_user,
            message="testuser1发送给testuser2的第一条消息"
        )
        self.second_message = Message.objects.create(
            sender=self.user,
            recipient=self.other_user,
            message="testuser1发送给testuser2的第二条消息"
        )
        self.third_message = Message.objects.create(
            sender=self.other_user,
            recipient=self.user,
            message="testuser2回复给testuser1的第一条消息"
        )

    def test_object_instance(self):
        """测试对象是否为Message类型"""
        assert isinstance(self.first_message, Message)
        assert isinstance(self.second_message, Message)
        assert isinstance(self.third_message, Message)

    def test_return_values(self):
        """测试对象的返回值"""
        assert str(self.first_message) == "testuser1发送给testuser2的第一条消息"
        assert self.first_message.message == "testuser1发送给testuser2的第一条消息"

    def test_conversation(self):
        """测试私信会话功能"""
        conversation = Message.objects.get_conversation(self.user, self.other_user)
        assert conversation.last().message == "testuser2回复给testuser1的第一条消息"

    def test_recent_conversation(self):
        """测试获取最近一次的私信互动的用户"""
        active_user = Message.objects.get_most_recent_conversation(self.user)
        assert active_user == self.other_user

    def test_single_marking_as_read(self):
        """测试私信标记为已读"""
        self.first_message.mark_as_read()
        read_message = Message.objects.filter(unread=False)
        assert read_message[0] == self.first_message
