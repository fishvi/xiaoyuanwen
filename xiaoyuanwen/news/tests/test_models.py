from test_plus.test import TestCase

from xiaoyuanwen.news.models import News


class TestNewsModels(TestCase):
    def setUp(self):
        self.user = self.make_user("testuser1")
        self.other_user = self.make_user("testuser2")
        self.first_news = News.objects.create(
            user=self.user,
            content="第一条动态"
        )
        self.second_news = News.objects.create(
            user=self.user,
            content="第二条动态"
        )
        self.comment_in_first_news = News.objects.create(
            user=self.other_user,
            content="评论第一条动态",
            reply=True,
            parent=self.first_news
        )

    def test__str__(self):
        """测试动态对象返回信息"""
        self.assertEqual(self.first_news.__str__(), "第一条动态")

    def test_switch_like(self):
        """测试点赞"""
        self.first_news.switch_like(self.other_user)
        assert self.first_news.liked_count() == 1
        assert self.other_user in self.first_news.get_liker()

    def test_reply_this(self):
        """测试评论"""
        initial_count = News.objects.count()
        self.first_news.reply_this(self.other_user, "评论第一条动态")
        assert News.objects.count() == initial_count + 1
        assert self.first_news.comment_count() == 2
        assert self.comment_in_first_news in self.first_news.get_thread()
