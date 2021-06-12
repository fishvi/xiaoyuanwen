from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    """用户详情页"""
    model = User
    template_name = "users/user_detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        """统计用户个人数据"""
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        context['moments_num'] = user.publisher.filter(reply=False).count()
        context['article_num'] = user.author.filter(status='P').count()
        context['comment_num'] = user.publisher.filter(reply=True).count() + user.comment_comments.all().count()
        context['question_num'] = user.q_author.all().count()
        context['answer_num'] = user.a_author.all().count()

        sent_users = user.sent_messages.all()  # 当前用户给哪些用户发送过私信
        receive_users = user.received_messages.all()  # 当前用户接收过来自哪些用户的私信
        sent_users_set = set()
        receive_users_set = set()
        for s in sent_users:
            sent_users_set.add(s.recipient.username)
        for r in receive_users:
            receive_users_set.add(r.sender.username)
        tmp = sent_users_set & receive_users_set
        context['interaction_num'] = user.liked_news.all().count() + user.qa_vote.all().count() + \
                                     context['comment_num'] + len(tmp)
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """更新用户个人信息"""
    model = User
    fields = ["nickname", "gender", "picture", "stu_id", "grade", "college", "location", "introduction", ]
    template_name = "users/user_form.html"

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user
