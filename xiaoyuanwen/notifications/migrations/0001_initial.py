# Generated by Django 2.2.3 on 2021-05-23 11:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('unread', models.BooleanField(db_index=True, default=True, verbose_name='是否未读')),
                ('slug', models.SlugField(blank=True, max_length=80, null=True, verbose_name='(URL)别名')),
                ('verb', models.CharField(choices=[('L', '赞了'), ('C', '评论了'), ('P', '回答了'), ('A', '采纳了回答'), ('R', '回复了')], max_length=1, verbose_name='通知类别')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('object_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': '通知',
                'verbose_name_plural': '通知',
                'ordering': ('-created_at',),
            },
        ),
    ]
