from django.test import Client
from django.urls import reverse
from test_plus.test import TestCase

from xiaoyuanwen.messager.models import Message


class TestMessagesViews(TestCase):
    def setUp(self):
        self.user = self.make_user("testuser1")
        self.other_user = self.make_user("testuser2")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="testuser1", password="password")
        self.other_client.login(username="testuser2", password="password")
        self.first_message = Message.objects.create(
            sender=self.user,
            recipient=self.other_user,
            message="testuser1发送给testuser2的第一条私信"
        )
        self.second_message = Message.objects.create(
            sender=self.user,
            recipient=self.other_user,
            message="testuser1发送给testuser2的第二条私信"
        )
        self.third_message = Message.objects.create(
            sender=self.other_user,
            recipient=self.user,
            message="testuser2回复给testuser1的第一条私信"
        )

    def test_user_messages(self):
        """测试testuser1的私信"""
        response = self.client.get(reverse("messager:messages_list"))
        assert response.status_code == 200
        assert str(response.context["message"]) == "testuser1发送给testuser2的第一条私信"

    def test_user_conversation(self):
        """测试私信会话"""
        response = self.client.get(reverse("messager:conversation_detail", kwargs={"username": self.user.username}))
        assert response.status_code == 200
        assert str(response.context["active"]) == "testuser1"

    def test_send_message_view(self):
        """测试发送私信"""
        message_count = Message.objects.count()
        request = self.client.post(
            reverse("messager:send_message"),
            {"to": "testuser2", "message": "私信内容"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert request.status_code == 200
        new_msm_count = Message.objects.count()
        assert new_msm_count == message_count + 1

    def test_wrong_requests_send_message(self):
        """测试使用错误的请求方式发送私信"""
        ajax_get_request = self.client.get(
            reverse("messager:send_message"),
            {"to": "testuser2", "message": "私信内容（AJAX-GET）"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        ajax_post_request = self.client.post(
            reverse("messager:send_message"),
            {"to": "testuser2", "message": "私信内容（AJAX-POST）"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        http_get_request = self.client.get(
            reverse("messager:send_message"),
            {"to": "testuser2", "message": "私信内容（HTTP-GET）"}
        )
        http_post_request = self.client.post(
            reverse("messager:send_message"),
            {"to": "testuser2", "message": "私信内容（HTTP-POST）"}
        )

        assert ajax_get_request.status_code == 405
        assert ajax_post_request.status_code == 200
        assert http_get_request.status_code == 400
        assert http_post_request.status_code == 400
