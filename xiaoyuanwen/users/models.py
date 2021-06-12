from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """自定义用户模型"""
    GENDER_CHOICE = (
        ('male', '男'),
        ('female', '女')
    )
    COLLEGE_CHOICE = (
        ('tx', '通信与信息工程学院'),
        ('jxj', '计算机科学与技术学院'),
        ('zdh', '自动化学院'),
        ('xj', '先进制造工程学院'),
        ('gd', '光电工程学院/重庆国际半导体学院'),
        ('rj', '软件工程学院'),
        ('sw', '生物信息学院'),
        ('l', '理学院'),
        ('jg', '经济管理学院/现代邮政学院'),
        ('cm', '传媒艺术学院'),
        ('wgy', '外国语学院'),
        ('gj', '国际学院'),
        ('af', '网络空间安全与信息法学院'),
        ('mks', '马克思主义学院'),
        ('ty', '体育学院'),
    )
    LOCATION_CHOICE = (
        ('bj', '北京'),
        ('tj', '天津'),
        ('hb1', '河北'),
        ('sx1', '山西'),
        ('nmg', '内蒙古'),
        ('ln', '辽宁'),
        ('jl', '吉林'),
        ('hlj', '黑龙江'),
        ('sh', '上海'),
        ('js', '江苏'),
        ('zj', '浙江'),
        ('ah', '安徽'),
        ('fj', '福建'),
        ('jx', '江西'),
        ('sd', '山东'),
        ('henan', '河南'),
        ('hb2', '湖北'),
        ('hn1', '湖南'),
        ('gd', '广东'),
        ('gx', '广西'),
        ('hn2', '海南'),
        ('cq', '重庆'),
        ('sc', '四川'),
        ('gz', '贵州'),
        ('yn', '云南'),
        ('xz', '西藏'),
        ('sx2', '陕西'),
        ('gs', '甘肃'),
        ('qh', '青海'),
        ('nx', '宁夏'),
        ('xj', '新疆'),
        ('tw', '台湾'),
        ('xg', '香港特别行政区'),
        ('am', '澳门特别行政区'),
        ('hw', '海外'),
    )

    nickname = models.CharField(max_length=6, null=True, blank=True, verbose_name='昵称')
    gender = models.CharField(choices=GENDER_CHOICE, max_length=10, null=True, blank=True, verbose_name='性别')
    picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name='头像')
    stu_id = models.PositiveIntegerField(unique=True, null=True, blank=True, verbose_name='学号')
    grade = models.CharField(max_length=4, null=True, blank=True, verbose_name='年级')
    college = models.CharField(choices=COLLEGE_CHOICE, max_length=20, null=True, blank=True, verbose_name='学院')
    location = models.CharField(choices=LOCATION_CHOICE, max_length=10, null=True, blank=True, verbose_name='家乡')
    introduction = models.CharField(max_length=20, default='这位同学很懒，还没有编辑个人简介',
                                    null=True, blank=True, verbose_name='个人简介')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        if self.nickname:
            return self.nickname
        return self.username
