from django.http import Http404
from django.shortcuts import get_object_or_404

from users.models import Profile


class UserIsNotAuthMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404("Вы уже авторизованны!")
        return super().dispatch(request, *args, **kwargs)


class IsNotFreelancerMixin:
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, owner_user=self.request.user)
        if profile.free_lancer_status == True:
            raise Http404("Вы исполнитель а не заказчик!")
        return super().dispatch(request, *args, **kwargs)


class IsFreeLancerMixin:
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, owner_user=self.request.user)
        if profile.free_lancer_status != True:
            raise Http404("Вы заказчик а не исполнитель!")
        return super().dispatch(request, *args, **kwargs)