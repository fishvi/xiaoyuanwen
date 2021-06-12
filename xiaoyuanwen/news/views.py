from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy

from xiaoyuanwen.news.models import News
from xiaoyuanwen.helpers import ajax_required, AuthorRequireMixin


class NewsListView(LoginRequiredMixin, ListView):
    """动态列表"""
    model = News
    paginate_by = 20
    template_name = 'news/news_list.html'

    def get_queryset(self):
        return News.objects.filter(reply=False).select_related('user', 'parent').prefetch_related('liked')


class NewsDeleteView(LoginRequiredMixin, AuthorRequireMixin, DeleteView):
    """删除动态"""
    model = News
    template_name = 'news/news_confirm_delete.html'
    message = "您的动态删除成功！"

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("news:list")


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_news(request):
    """发表动态（AJAX POST）"""
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        html = render_to_string('news/news_single.html', {'news': posted, 'request': request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空！")


@login_required
@ajax_required
@require_http_methods(['POST'])
def like(request):
    """点赞动态（AJAX POST）"""
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    news.switch_like(request.user)
    return JsonResponse({'likes': news.liked_count()})


@login_required
@ajax_required
@require_http_methods(['GET'])
def get_thread(request):
    """返回动态的评论（AJAX GET）"""
    news_id = request.GET['news']
    news = News.objects.select_related('user').get(pk=news_id)
    news_html = render_to_string('news/news_single.html', {'news': news})
    thread_html = render_to_string('news/news_thread.html', {'thread': news.get_thread()})
    return JsonResponse({
        "uuid": news_id,
        "news": news_html,
        "thread": thread_html
    })


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_comment(request):
    """发表评论（AJAX POST）"""
    post = request.POST['reply'].strip()
    parent_id = request.POST['parent']
    parent = News.objects.get(pk=parent_id)
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({'comments': parent.comment_count()})
    else:
        return HttpResponseBadRequest("内容不能为空！")


@login_required
@ajax_required
@require_http_methods(['POST'])
def update_interactions(request):
    """更新互动信息（AJAX POST）"""
    date_point = request.POST['id_value']
    news = News.objects.get(pk=date_point)
    return JsonResponse({'likes': news.liked_count(), 'comments': news.comment_count()})
