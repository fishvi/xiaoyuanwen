from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from xiaoyuanwen.messager.models import Message
from xiaoyuanwen.helpers import ajax_required
from xiaoyuanwen.notifications.views import notification_handler


class MessagesListView(LoginRequiredMixin, ListView):
    """所有用户的私信列表"""
    model = Message
    template_name = "messager/message_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        """获取除当前登录用户外的所有用户"""
        context = super(MessagesListView, self).get_context_data()
        context["users_list"] = get_user_model().objects.filter(is_active=True).exclude(
            username=self.request.user
        ).order_by('-last_login')[:8]
        last_conversation = Message.objects.get_most_recent_conversation(self.request.user)
        context["active"] = last_conversation.username
        return context

    def get_queryset(self):
        """最近私信互动的内容"""
        active_user = Message.objects.get_most_recent_conversation(self.request.user)
        return Message.objects.get_conversation(active_user, self.request.user)


class ConversationListView(MessagesListView):
    """与指定用户的私信内容"""
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ConversationListView, self).get_context_data()
        context["active"] = self.kwargs["username"]
        return context

    def get_queryset(self):
        active_user = get_object_or_404(get_user_model(), username=self.kwargs["username"])
        return Message.objects.get_conversation(active_user, self.request.user)


@login_required
@ajax_required
@require_http_methods(["POST"])
def send_message(request):
    """私信聊天"""
    sender = request.user
    recipient_username = request.POST["to"]
    recipient = get_user_model().objects.get(username=recipient_username)
    message = request.POST["message"]
    if len(message.strip()) != 0 and sender != recipient:
        msg = Message.objects.create(
            sender=sender,
            recipient=recipient,
            message=message
        )
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'message': render_to_string('messager/single_message.html', {'message': msg}),
            'sender': sender.username
        }
        async_to_sync(channel_layer.group_send)(recipient_username, payload)
        notification_handler(sender, recipient, 'R', msg)
        return render(request, 'messager/single_message.html', {"message": msg})
    return HttpResponse()
