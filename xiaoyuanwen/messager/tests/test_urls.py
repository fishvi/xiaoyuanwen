from django.urls import reverse, resolve
from test_plus.test import TestCase


class TestMessagerURLs(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_messages_list_reverse(self):
        self.assertEqual(reverse('messager:messages_list'), '/messager/')

    def test_messages_list_resolve(self):
        self.assertEqual(resolve('/messager/').view_name, 'messager:messages_list')

    def test_send_message_reverse(self):
        self.assertEqual(reverse('messager:send_message'), '/messager/send-message/')

    def test_send_message_resolve(self):
        self.assertEqual(resolve('/messager/send-message/').view_name, 'messager:send_message')

    def test_conversation_detail_reverse(self):
        self.assertEqual(reverse('messager:conversation_detail', kwargs={'username': 'testuser'}),
                         '/messager/testuser/')

    def test_conversation_detail_resolve(self):
        self.assertEqual(resolve('/messager/testuser/').view_name, 'messager:conversation_detail')
