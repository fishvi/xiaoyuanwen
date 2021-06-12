from django.urls import reverse, resolve
from test_plus.test import TestCase


class TestArticlesURLs(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_list_reverse(self):
        self.assertEqual(reverse('articles:list'), '/articles/')

    def test_list_resolve(self):
        self.assertEqual(resolve('/articles/').view_name, 'articles:list')

    def test_write_new_reverse(self):
        self.assertEqual(reverse('articles:write_new'), '/articles/write-new-article/')

    def test_write_new_resolver(self):
        self.assertEqual(resolve('/articles/write-new-article/').view_name, 'articles:write_new')

    def test_drafts_reverse(self):
        self.assertEqual(reverse('articles:drafts'), '/articles/drafts/')

    def test_drafts_resolve(self):
        self.assertEqual(resolve('/articles/drafts/').view_name, 'articles:drafts')

    def test_article_reverse(self):
        self.assertEqual(reverse('articles:article', kwargs={'slug': 'test-title'}), '/articles/test-title/')

    def test_article_resolve(self):
        self.assertEqual(resolve('/articles/test-title/').view_name, 'articles:article')

    def test_edit_article_reverse(self):
        self.assertEqual(reverse('articles:edit_article', kwargs={'pk': 1}), '/articles/edit/1/')

    def test_edit_article_resolve(self):
        self.assertEqual(resolve('/articles/edit/1/').view_name, 'articles:edit_article')

    def test_delete_article_reverse(self):
        self.assertEqual(reverse('articles:delete_article', kwargs={'pk': 1}), '/articles/delete/1/')

    def test_delete_article_resolve(self):
        self.assertEqual(resolve('/articles/delete/1/').view_name, 'articles:delete_article')
