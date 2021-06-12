from test_plus.test import TestCase


class TestUser(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        """测试用户对象返回信息"""
        self.assertEqual(self.user.__str__(), 'testuser')

    def test_get_absolute_url(self):
        """测试用户对象专属详情页"""
        self.assertEqual(self.user.get_absolute_url(), '/users/testuser/')

    def test_get_profile_name(self):
        """测试获取用户名称"""
        assert self.user.get_profile_name() == 'testuser'
        self.user.nickname = '昵称'
        assert self.user.get_profile_name() == '昵称'
