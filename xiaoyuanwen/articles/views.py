from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django_comments.signals import comment_was_posted

from xiaoyuanwen.articles.models import Article
from xiaoyuanwen.articles.forms import ArticleForm
from xiaoyuanwen.helpers import AuthorRequireMixin
from xiaoyuanwen.notifications.views import notification_handler


class ArticlesListView(LoginRequiredMixin, ListView):
    """已发布的文章列表"""
    model = Article
    paginate_by = 10
    context_object_name = "articles"
    template_name = "articles/article_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self):
        return Article.objects.get_published()


class DraftListView(ArticlesListView):
    """草稿箱中的文章列表"""
    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).get_drafts()


@method_decorator(cache_page(60 * 60), name='get')
class ArticleCreateView(LoginRequiredMixin, CreateView):
    """发表文章"""
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_create.html"
    message = "您的文章已发表成功！"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("articles:list")


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """文章详情"""
    model = Article
    template_name = 'articles/article_detail.html'

    def get_queryset(self):
        return Article.objects.select_related('user').filter(slug=self.kwargs['slug'])


class ArticleEditView(LoginRequiredMixin, AuthorRequireMixin, UpdateView):
    """编辑文章"""
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_update.html"
    message = "您的文章编辑成功！"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("articles:article", kwargs={'slug': self.get_object().slug})


class ArticleDeleteView(LoginRequiredMixin, AuthorRequireMixin, DeleteView):
    """删除文章"""
    model = Article
    template_name = 'articles/article_confirm_delete.html'
    message = "您的文章删除成功！"

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("articles:list")


def notify_comment(**kwargs):
    """文章有评论时通知文章作者"""
    actor = kwargs['request'].user
    obj = kwargs['comment'].content_object
    if actor.username != obj.user.username:
        notification_handler(actor, obj.user, 'C', obj)


comment_was_posted.connect(receiver=notify_comment)
