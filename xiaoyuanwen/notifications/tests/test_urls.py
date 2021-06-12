from django.urls import reverse, resolve
from test_plus.test import TestCase


class TestNotificationsURLs(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_unread_reverse(self):
        self.assertEqual(reverse('notifications:unread'), '/notifications/')

    def test_unread_resolve(self):
        self.assertEqual(resolve('/notifications/').view_name, 'notifications:unread')

    def test_latest_notifications_reverse(self):
        self.assertEqual(reverse('notifications:latest_notifications'), '/notifications/latest-notifications/')

    def test_latest_notifications_resolve(self):
        self.assertEqual(resolve('/notifications/latest-notifications/').view_name, 'notifications:latest_notifications')

    def test_mark_as_read_reverse(self):
        self.assertEqual(reverse('notifications:mark_as_read', kwargs={'slug': 'testuser'}),
                         '/notifications/mark-as-read/testuser/')

    def test_mark_as_read_resolve(self):
        self.assertEqual(resolve('/notifications/mark-as-read/testuser/').view_name, 'notifications:mark_as_read')

    def test_mark_all_read_reverse(self):
        self.assertEqual(reverse('notifications:mark_all_read'), '/notifications/mark-all-read/')

    def test_mark_all_read_resolve(self):
        self.assertEqual(resolve('/notifications/mark-all-read/').view_name, 'notifications:mark_all_read')
