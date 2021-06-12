from test_plus.test import TestCase

from xiaoyuanwen.articles.models import Article


class TestArticleModels(TestCase):
    def setUp(self):
        self.user = self.make_user("testuser")
        self.article = Article.objects.create(
            title="第一篇文章",
            content="test_article_content_1",
            status="P",
            user=self.user
        )
        self.article_in_draft = Article.objects.create(
            title="第二篇文章",
            content="test_article_content_2",
            user=self.user
        )

    def test_object_instance(self):
        """测试对象是否为Article类型"""
        assert isinstance(self.article, Article)
        assert isinstance(self.article_in_draft, Article)
        assert isinstance(Article.objects.get_published()[0], Article)
        assert isinstance(Article.objects.get_drafts()[0], Article)

    def test_return_values(self):
        """测试返回值"""
        assert self.article.status == "P"
        assert self.article_in_draft.status == "D"
        assert str(self.article) == "第一篇文章"
        assert self.article in Article.objects.get_published()
        assert Article.objects.get_published()[0].title == "第一篇文章"
        assert self.article_in_draft in Article.objects.get_drafts()
        assert Article.objects.get_drafts()[0].title == "第二篇文章"
