# Generated by Django 2.2.3 on 2021-05-23 11:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='动态内容')),
                ('reply', models.BooleanField(default=False, verbose_name='是否为评论')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '动态',
                'verbose_name_plural': '动态',
                'ordering': ('-created_at',),
            },
        ),
    ]
