from django.test import Client
from django.urls import reverse
from test_plus.test import TestCase

from xiaoyuanwen.qa.models import Question, Answer


class TestQaViews(TestCase):
    def setUp(self):
        self.user = self.make_user("testuser1")
        self.other_user = self.make_user("testuser2")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="testuser1", password="password")
        self.other_client.login(username="testuser2", password="password")
        self.question_1 = Question.objects.create(
            user=self.user,
            title="问题1",
            content="问题1的内容",
            tags="测试1,测试2"
        )
        self.question_2 = Question.objects.create(
            user=self.user,
            title="问题2",
            content="问题2的内容",
            has_answer=True,
            tags="测试1,测试2"
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question_2,
            content="问题2的采纳答案",
            is_answer=True
        )

    def test_question_list(self):
        """测试问题列表"""
        response = self.client.get(reverse("qa:all_q"))
        assert response.status_code == 200
        assert "问题1" in str(response.context["questions"])
        assert "问题2" in str(response.context["questions"])

    def test_create_question_view(self):
        """测试提问"""
        current_count = Question.objects.count()
        response = self.client.post(
            reverse("qa:ask_question"),
            {
                "title": "问题",
                "content": "内容",
                "status": "O",
                "tags": "测试标签"
            })
        assert response.status_code == 302
        new_question = Question.objects.first()
        assert new_question.title == "问题"
        assert Question.objects.count() == current_count + 1

    def test_answered_question(self):
        """测试已有采纳答案问题的列表"""
        response = self.client.get(reverse("qa:answered_q"))
        assert response.status_code == 200
        assert "问题2" in str(response.context["questions"])

    def test_unanswered_question(self):
        """测试没有采纳答案问题的列表"""
        response = self.client.get(reverse("qa:unanswered_q"))
        assert response.status_code == 200
        assert "问题1" in str(response.context["questions"])

    def test_answer_question(self):
        """测试回答问题"""
        current_answer_count = Answer.objects.count()
        response = self.client.post(
            reverse("qa:propose_answer", kwargs={"question_id": self.question_1.id}),
            {
                "content": "问题1的回答"
            })
        assert response.status_code == 302
        assert Answer.objects.count() == current_answer_count + 1

    def test_upvote_question(self):
        """测试点赞问题"""
        response = self.client.post(
            reverse("qa:question_vote"),
            {
                "value": "U",
                "question": self.question_1.id
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert response.status_code == 200

    def test_downvote_question(self):
        """测试踩问题"""
        response = self.client.post(
            reverse("qa:question_vote"),
            {
                "value": "D",
                "question": self.question_1.id
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert response.status_code == 200

    def test_upvote_answer(self):
        """测试点赞回答"""
        response = self.client.post(
            reverse("qa:answer_vote"),
            {
                "value": "U",
                "answer": self.answer.uuid_id
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert response.status_code == 200

    def test_downvote_answer(self):
        """测试踩回答"""
        response = self.client.post(
            reverse("qa:answer_vote"),
            {
                "value": "D",
                "answer": self.answer.uuid_id
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert response.status_code == 200

    def test_accept_answer(self):
        """测试采纳答案"""
        response = self.client.post(
            reverse("qa:accept_answer"),
            {
                "answer": self.answer.uuid_id
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert response.status_code == 200
