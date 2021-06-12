import uuid
from collections import Counter

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager
from slugify import slugify

from xiaoyuanwen.users.models import User


class Vote(models.Model):
    """投票模型"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="qa_vote", on_delete=models.CASCADE, verbose_name="用户")
    value = models.BooleanField(default=True, verbose_name="赞同或反对")
    content_type = models.ForeignKey(ContentType, related_name="votes_on", on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    vote = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "投票"
        verbose_name_plural = verbose_name
        unique_together = ("user", "content_type", "object_id")  # 联合唯一键
        index_together = ("content_type", "object_id")  # 联合唯一索引


class QuestionQuerySet(models.query.QuerySet):
    """自定义QuerySet，提高模型类的可用性"""
    def get_answered(self):
        """已采纳答案的问题"""
        return self.filter(has_answer=True).select_related('user')

    def get_unanswered(self):
        """未采纳答案的问题"""
        return self.filter(has_answer=False).select_related('user')

    def get_counted_tags(self):
        """统计所有问题中每一个标签的数量"""
        tag_dict = {}
        query = self.all().annotate(tagged=models.Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class Question(models.Model):
    """问题模型"""
    STATUS = (
        ("O", "Open"),
        ("C", "Close"),
    )

    user = models.ForeignKey(User, related_name="q_author", on_delete=models.CASCADE, verbose_name="提问者")
    title = models.CharField(max_length=255, unique=True, verbose_name="标题")
    slug = models.SlugField(max_length=80, null=True, blank=True, verbose_name="(URL)别名")
    status = models.CharField(max_length=1, choices=STATUS, default="O", verbose_name="问题状态")
    content = MarkdownxField(verbose_name="内容")
    tags = TaggableManager(help_text="多个标签使用英文逗号隔开", verbose_name="标签")
    has_answer = models.BooleanField(default=False, verbose_name="是否已采纳回答")
    votes = GenericRelation(Vote, verbose_name="投票情况")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = "问题"
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        """得票数（支持 - 反对）"""
        dic = Counter(self.votes.values_list('value', flat=True))
        return dic[True] - dic[False]

    def get_answers(self):
        """获取所有的回答"""
        return Answer.objects.filter(question=self).select_related('user', 'question')

    def count_answers(self):
        """回答数量"""
        return self.get_answers().count()

    def get_upvoters(self):
        """赞同的用户"""
        return [vote.user for vote in self.votes.filter(value=True).select_related('user').prefetch_related('vote')]

    def get_downvoters(self):
        """反对的用户"""
        return [vote.user for vote in self.votes.filter(value=False).select_related('user').prefetch_related('vote')]


class Answer(models.Model):
    """回答模型"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="a_author", on_delete=models.CASCADE, verbose_name="回答者")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="问题")
    content = MarkdownxField(verbose_name="内容")
    is_answer = models.BooleanField(default=False, verbose_name="是否被采纳回答")
    votes = GenericRelation(Vote, verbose_name="投票情况")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "回答"
        verbose_name_plural = verbose_name
        ordering = ("-is_answer", "-created_at")

    def __str__(self):
        return self.content

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        """得票数（支持 - 反对）"""
        dic = Counter(self.votes.values_list('value', flat=True))
        return dic[True] - dic[False]

    def get_upvoters(self):
        """赞同的用户"""
        return [vote.user for vote in self.votes.filter(value=True).select_related('user').prefetch_related('vote')]

    def get_downvoters(self):
        """反对的用户"""
        return [vote.user for vote in self.votes.filter(value=False).select_related('user').prefetch_related('vote')]

    def accept_answer(self):
        """采纳回答"""
        answer_set = Answer.objects.filter(question=self.question)
        answer_set.update(is_answer=False)
        self.is_answer = True
        self.save()
        self.question.has_answer = True
        self.question.save()
