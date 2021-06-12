from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from xiaoyuanwen.helpers import ajax_required
from xiaoyuanwen.qa.models import Question, Answer
from xiaoyuanwen.qa.forms import QuestionForm
from xiaoyuanwen.notifications.views import notification_handler


class QuestionListView(LoginRequiredMixin, ListView):
    """所有问题列表"""
    model = Question
    paginate_by = 10
    context_object_name = "questions"
    template_name = "qa/question_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context["popular_tags"] = Question.objects.get_counted_tags()
        context["active"] = "all"
        return context

    def get_queryset(self):
        return Question.objects.select_related('user')


class AnsweredQuestionListView(QuestionListView):
    """已有采纳答案的问题列表"""
    def get_queryset(self):
        return Question.objects.get_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AnsweredQuestionListView, self).get_context_data()
        context["active"] = "answered"
        return context


class UnansweredQuestionListView(QuestionListView):
    """没有采纳答案的问题列表"""
    def get_queryset(self):
        return Question.objects.get_unanswered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UnansweredQuestionListView, self).get_context_data()
        context["active"] = "unanswered"
        return context


@method_decorator(cache_page(60 * 60), name='get')
class CreateQuestionView(LoginRequiredMixin, CreateView):
    """用户提问"""
    model = Question
    form_class = QuestionForm
    template_name = "qa/question_form.html"
    message = "您的问题已成功提交！"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("qa:unanswered_q")


class QuestionDetailView(LoginRequiredMixin, DetailView):
    """问题详情页"""
    model = Question
    context_object_name = "question"
    template_name = "qa/question_detail.html"

    def get_queryset(self):
        return Question.objects.select_related('user').filter(pk=self.kwargs['pk'])


@method_decorator(cache_page(60 * 60), name='get')
class CreateAnswerView(LoginRequiredMixin, CreateView):
    """回答问题"""
    model = Answer
    fields = ['content']
    message = "您的回答已提交！"
    template_name = "qa/answer_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        question_id = self.kwargs['question_id']
        question = Question.objects.get(pk=question_id)
        if self.request.user.username != question.user.username:
            notification_handler(self.request.user, question.user, 'P', question)
        return reverse_lazy("qa:question_detail", kwargs={"pk": self.kwargs['question_id']})


@login_required
@ajax_required
@require_http_methods(["POST"])
def question_vote(request):
    """给问题投票（AJAX POST）"""
    question_id = request.POST["question"]
    value = True if request.POST["value"] == "U" else False
    question = Question.objects.get(pk=question_id)
    users = question.votes.values_list("user", flat=True)
    if request.user.pk in users and (question.votes.get(user=request.user).value == value):
        question.votes.get(user=request.user).delete()
    else:
        question.votes.update_or_create(user=request.user, defaults={"value": value})
    return JsonResponse({"votes": question.total_votes()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def answer_vote(request):
    """给回答投票（AJAX POST）"""
    answer_id = request.POST["answer"]
    value = True if request.POST["value"] == "U" else False
    answer = Answer.objects.get(pk=answer_id)
    users = answer.votes.values_list("user", flat=True)
    if request.user.pk in users and (answer.votes.get(user=request.user).value == value):
        answer.votes.get(user=request.user).delete()
    else:
        answer.votes.update_or_create(user=request.user, defaults={"value": value})
    return JsonResponse({"votes": answer.total_votes()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def accept_answer(request):
    """采纳答案（AJAX POST）"""
    answer_id = request.POST["answer"]
    answer = Answer.objects.get(pk=answer_id)
    if answer.question.user.username != request.user.username:
        raise PermissionDenied
    answer.accept_answer()
    if request.user.username != answer.user.username:
        notification_handler(request.user, answer.user, 'A', answer)
    return JsonResponse({"status": "true"})
