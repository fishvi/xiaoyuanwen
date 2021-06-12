from django.urls import reverse, resolve
from test_plus.test import TestCase


class TestQaURLs(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_unanswered_q_reverse(self):
        self.assertEqual(reverse('qa:unanswered_q'), '/qa/')

    def test_unanswered_q_resolve(self):
        self.assertEqual(resolve('/qa/').view_name, 'qa:unanswered_q')

    def test_answered_q_reverse(self):
        self.assertEqual(reverse('qa:answered_q'), '/qa/answered/')

    def test_answered_q_resolve(self):
        self.assertEqual(resolve('/qa/answered/').view_name, 'qa:answered_q')

    def test_all_q_reverse(self):
        self.assertEqual(reverse('qa:all_q'), '/qa/indexed/')

    def test_all_q_resolve(self):
        self.assertEqual(resolve('/qa/indexed/').view_name, 'qa:all_q')

    def test_ask_question_reverse(self):
        self.assertEqual(reverse('qa:ask_question'), '/qa/ask-question/')

    def test_ask_question_resolve(self):
        self.assertEqual(resolve('/qa/ask-question/').view_name, 'qa:ask_question')

    def test_question_detail_reverse(self):
        self.assertEqual(reverse('qa:question_detail', kwargs={'pk': 1}), '/qa/question-detail/1/')

    def test_question_detail_resolve(self):
        self.assertEqual(resolve('/qa/question-detail/1/').view_name, 'qa:question_detail')

    def test_propose_answer_reverse(self):
        self.assertEqual(reverse('qa:propose_answer', kwargs={'question_id': 1}), '/qa/propose-answer/1/')

    def test_propose_answer_resolve(self):
        self.assertEqual(resolve('/qa/propose-answer/1/').view_name, 'qa:propose_answer')

    def test_question_vote_reverse(self):
        self.assertEqual(reverse('qa:question_vote'), '/qa/question/vote/')

    def test_question_vote_resolve(self):
        self.assertEqual(resolve('/qa/question/vote/').view_name, 'qa:question_vote')

    def test_answer_vote_reverse(self):
        self.assertEqual(reverse('qa:answer_vote'), '/qa/answer/vote/')

    def test_answer_vote_resolve(self):
        self.assertEqual(resolve('/qa/answer/vote/').view_name, 'qa:answer_vote')

    def test_accept_answer_reverse(self):
        self.assertEqual(reverse('qa:accept_answer'), '/qa/accept-answer/')

    def test_accept_answer_resolve(self):
        self.assertEqual(resolve('/qa/accept-answer/').view_name, 'qa:accept_answer')
