from django.contrib import admin

from xiaoyuanwen.qa.models import Question, Answer
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    pass


class AnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
