import uuid

from django.db import models
from django.contrib.auth import get_user_model

from xiaoyuanwen.users.models import User


class MessageQuerySet(models.query.QuerySet):
    """自定义查询集"""
    def get_conversation(self, sender, recipient):
        """获取私信聊天记录"""
        qs_one = self.filter(sender=sender, recipient=recipient).select_related('sender', 'recipient')
        qs_two = self.filter(sender=recipient, recipient=sender).select_related('sender', 'recipient')
        return qs_one.union(qs_two).order_by('created_at')

    def get_most_recent_conversation(self, recipient):
        """获取最近一次私信互动的用户"""
        try:
            qs_sent = self.filter(sender=recipient).select_related('sender', 'recipient')
            qs_received = self.filter(recipient=recipient).select_related('sender', 'recipient')
            qs = qs_sent.union(qs_received).latest("created_at")
            if qs.sender == recipient:
                return qs.recipient
            return qs.sender
        except self.model.DoesNotExist:
            return get_user_model().objects.get(username=recipient.username)


class Message(models.Model):
    """私信模型"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, related_name="sent_messages", null=True, blank=True,
                               on_delete=models.SET_NULL, verbose_name="发送者")
    recipient = models.ForeignKey(User, related_name="received_messages", null=True, blank=True,
                                  on_delete=models.SET_NULL, verbose_name="接收者")
    message = models.TextField(null=True, blank=True, verbose_name="内容")
    unread = models.BooleanField(default=True, db_index=True, verbose_name="是否未读")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="创建时间")
    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = "私信"
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.message

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
