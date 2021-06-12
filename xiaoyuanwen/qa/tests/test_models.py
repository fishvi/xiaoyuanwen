from test_plus.test import TestCase

from xiaoyuanwen.qa.models import Question, Answer


class TestQaModels(TestCase):
    def setUp(self):
        self.user = self.make_user("testuser1")
        self.other_user = self.make_user("testuser2")
        self.question_1 = Question.objects.create(
            user=self.user,
            title="问题1",
            content="问题1的内容",
            tags="测试1,测试2"
        )
        self.question_2 = Question.objects.create(
            user=self.other_user,
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

    def test_question_str(self):
        """测试问题对象返回信息"""
        assert isinstance(self.question_1, Question)
        assert str(self.question_1) == "问题1"

    def test_answer_str(self):
        """测试答案对象返回信息"""
        assert isinstance(self.answer, Answer)
        assert str(self.answer) == "问题2的采纳答案"

    def test_vote_question(self):
        """测试给问题投票"""
        self.question_1.votes.update_or_create(user=self.user, defaults={'value': True})
        self.question_1.votes.update_or_create(user=self.other_user, defaults={'value': True})
        assert self.question_1.total_votes() == 2

    def test_vote_answer(self):
        """测试给回答投票"""
        self.answer.votes.update_or_create(user=self.user, defaults={'value': True})
        self.answer.votes.update_or_create(user=self.other_user, defaults={'value': True})
        assert self.answer.total_votes() == 2

    def test_get_question_voters(self):
        """测试获取问题的投票者"""
        self.question_1.votes.update_or_create(user=self.user, defaults={'value': True})
        self.question_1.votes.update_or_create(user=self.other_user, defaults={'value': False})
        assert self.user in self.question_1.get_upvoters()
        assert self.other_user in self.question_1.get_downvoters()

    def test_get_answer_voters(self):
        """测试获取回答的投票者"""
        self.answer.votes.update_or_create(user=self.user, defaults={'value': True})
        self.answer.votes.update_or_create(user=self.other_user, defaults={'value': False})
        assert self.user in self.answer.get_upvoters()
        assert self.other_user in self.answer.get_downvoters()

    def test_unanswered_question(self):
        """测试获取没有采纳答案的问题"""
        assert self.question_1 == Question.objects.get_unanswered()[0]

    def test_answered_question(self):
        """测试获取已有采纳答案的问题"""
        assert self.question_2 == Question.objects.get_answered()[0]

    def test_get_answers(self):
        """测试获取回答"""
        assert self.answer == self.question_2.get_answers()[0]
        assert self.question_2.count_answers() == 1

    def test_get_accepted_answer(self):
        """测试获取被采纳的答案"""
        answer_1 = Answer.objects.create(
            user=self.user,
            question=self.question_1,
            content="回答1"
        )
        answer_2 = Answer.objects.create(
            user=self.user,
            question=self.question_1,
            content="回答2"
        )
        answer_3 = Answer.objects.create(
            user=self.user,
            question=self.question_1,
            content="回答3"
        )
        self.assertFalse(answer_1.is_answer)
        self.assertFalse(answer_2.is_answer)
        self.assertFalse(answer_3.is_answer)
        self.assertFalse(self.question_1.has_answer)
        answer_1.accept_answer()
        self.assertTrue(answer_1.is_answer)
        self.assertFalse(answer_2.is_answer)
        self.assertFalse(answer_3.is_answer)
        self.assertTrue(self.question_1.has_answer)
