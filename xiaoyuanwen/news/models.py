import uuid

from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from xiaoyuanwen.users.models import User
from xiaoyuanwen.notifications.views import notification_handler


class News(models.Model):
    """动态模型"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='publisher', verbose_name='用户')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='thread', verbose_name='自关联')
    content = models.TextField(verbose_name='动态内容')
    liked = models.ManyToManyField(User, related_name='liked_news', verbose_name='点赞用户')
    reply = models.BooleanField(default=False, verbose_name='是否为评论')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '动态'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.content

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(News, self).save()
        if not self.reply:
            channel_layer = get_channel_layer()
            payload = {
                'type': 'receive',
                'key': 'additional_news',
                'actor_name': self.user.username
            }
            async_to_sync(channel_layer.group_send)('notifications', payload)

    def switch_like(self, user):
        """点赞或取消赞"""
        if user in self.liked.all():
            self.liked.remove(user)
        else:
            self.liked.add(user)
            if user.username != self.user.username:
                notification_handler(user, self.user, 'L', self, id_value=str(self.uuid_id), key='social_update')

    def get_parent(self):
        """返回自关联中的上级记录或者本身"""
        if self.parent:
            return self.parent
        else:
            return self

    def reply_this(self, user, text):
        """
        评论动态
        :param user: 登录的用户
        :param text: 评论的内容
        :return: None
        """
        parent = self.get_parent()
        News.objects.create(
            user=user,
            content=text,
            reply=True,
            parent=parent
        )
        if user.username != parent.user.username:
            notification_handler(user, parent.user, 'R', parent, id_value=str(parent.uuid_id), key='social_update')

    def get_thread(self):
        """返回关联到当前动态的所有评论"""
        parent = self.get_parent()
        return parent.thread.all()

    def comment_count(self):
        """评论数"""
        return self.get_thread().count()

    def liked_count(self):
        """点赞数"""
        return self.liked.count()

    def get_liker(self):
        """所有的点赞用户"""
        return self.liked.all()
