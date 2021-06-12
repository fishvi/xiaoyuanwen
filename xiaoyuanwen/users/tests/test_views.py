from django.test import RequestFactory
from test_plus.test import TestCase

from xiaoyuanwen.users.views import UserUpdateView


class BaseUserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = self.make_user()


class TestUserUpdateView(BaseUserTestCase):
    def setUp(self):
        super().setUp()
        self.view = UserUpdateView()
        request = self.factory.get('/fake-url')
        request.user = self.user
        self.view.request = request

    def test_get_success_url(self):
        """测试用户更新信息后跳转页"""
        self.assertEqual(self.view.get_success_url(), '/users/testuser/')

    def test_get_object(self):
        """测试获取用户对象"""
        self.assertEqual(self.view.get_object(), self.user)
