import tempfile

from PIL import Image
from test_plus.test import TestCase
from django.urls import reverse
from django.test import override_settings

from xiaoyuanwen.articles.models import Article


class TestArticlesViews(TestCase):
    @staticmethod
    def get_temp_img():
        """生成一个文章图片并读取"""
        size = (200, 200)
        color = (255, 0, 0, 0)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            image = Image.new("RGB", size, color)
            image.save(f, "PNG")
        return open(f.name, mode="rb")

    def setUp(self):
        self.user = self.make_user("testuser")
        self.client.login(username="testuser", password="password")
        self.article = Article.objects.create(
            title="第一篇文章",
            content="test_article_content",
            status="P",
            user=self.user
        )
        self.test_image = self.get_temp_img()

    def tearDown(self):
        self.test_image.close()

    def test_articles_list(self):
        """测试文章列表"""
        response = self.client.get(reverse("articles:list"))
        assert response.status_code == 200
        assert self.article in response.context["articles"]

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_article(self):
        """测试发表文章"""
        current_count = Article.objects.count()
        response = self.client.post(reverse("articles:write_new"),
                                    {
                                        "title": "title_1",
                                        "content": "content_1",
                                        "image": self.test_image,
                                        "tags": "test1",
                                        "status": "P"
                                    })
        assert response.status_code == 302
        assert Article.objects.count() == current_count + 1

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_article_draft(self):
        """测试草稿箱"""
        response1 = self.client.post(reverse("articles:write_new"),
                                     {
                                         "title": "title_2",
                                         "content": "cotent_2",
                                         "image": self.test_image,
                                         "tags": "test2",
                                         "status": "D"
                                     })
        response2 = self.client.get(reverse("articles:drafts"))
        assert response1.status_code == 302
        assert response2.status_code == 200
        assert response2.context["articles"][0].slug == "title-2"

    def test_delete_article(self):
        """测试删除文章"""
        initial_count = Article.objects.count()
        response = self.client.post(reverse("articles:delete_article", kwargs={"pk": self.article.pk}))
        assert response.status_code == 302
        assert Article.objects.count() == initial_count - 1
