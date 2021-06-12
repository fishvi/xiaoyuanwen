from functools import wraps
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.exceptions import PermissionDenied


def ajax_required(f):
    """验证是否为AJAX请求"""
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest("不是Ajax请求！")
        return f(request, *args, **kwargs)
    return wrap


class AuthorRequireMixin(View):
    """验证当前用户是否为原作者"""
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
