from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from xiaoyuanwen.notifications.models import Notification


class NotificationUnreadListView(LoginRequiredMixin, ListView):
    """未读通知列表"""
    model = Notification
    context_object_name = "notification_list"
    template_name = "notifications/notification_list.html"

    def get_queryset(self, **kwargs):
        return self.request.user.notifications.unread()


@login_required
def get_latest_notifications(request):
    """最近的未读通知"""
    notifications = request.user.notifications.get_most_recent()
    return render(request, 'notifications/most_recent.html', {'notifications': notifications})


@login_required
def mark_as_read(request, slug):
    """将某条通知标为已读"""
    notification = get_object_or_404(Notification, slug=slug)
    notification.mark_as_read()
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('notifications:unread')


@login_required
def mark_all_as_read(request):
    """将所有通知标为已读"""
    request.user.notifications.mark_all_as_read()
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('notifications:unread')


def notification_handler(actor, recipient, verb, action_object, **kwargs):
    """
    通知处理器
    :param actor: request.user对象
    :param recipient: User Instance 接收者实例，一个或多个接收者
    :param verb: str 通知类别
    :param action_object: Instance 动作对象的实例
    :param kwargs: key, id_value等
    :return: None
    """
    key = kwargs.get('key', 'notification')
    id_value = kwargs.get('id_value', None)
    Notification.objects.create(
        actor=actor,
        recipient=recipient,
        verb=verb,
        action_object=action_object
    )
    channel_layer = get_channel_layer()
    if action_object.__class__.__name__ == 'Message':
        action_object_username = action_object.sender.username
    else:
        action_object_username = action_object.user.username
    payload = {
        'type': 'receive',
        'key': key,
        'actor_name': actor.username,
        'action_object': action_object_username,
        'id_value': id_value
    }
    async_to_sync(channel_layer.group_send)('notifications', payload)
