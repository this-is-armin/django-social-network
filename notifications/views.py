from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from utils.pagination import get_pagination_context
from .models import Notification


class NotificationsView(LoginRequiredMixin, View):
    template_name = 'notifications/notifications.html'

    def get(self, request):
        notifications = request.user.notifications.all()
        can_read_all = notifications.filter(is_read=False).exists()
        return render(request, self.template_name, {
            'page_obj': get_pagination_context(request, notifications, 10),
            'can_read_all': can_read_all,
        })


class NotificationReadView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        notification = get_object_or_404(Notification, pk=kwargs['pk'], to_user=request.user)

        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return redirect('notifications:notifications')


class NotificationReadAllView(LoginRequiredMixin, View):
    def get(self, request):
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return redirect('notifications:notifications')


class NotificationDeleteView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        get_object_or_404(Notification, pk=kwargs['pk'], to_user=request.user).delete()
        return redirect('notifications:notifications')


class NotificationDeleteAllView(LoginRequiredMixin, View):
    def get(self, request):
        request.user.notifications.all().delete()
        return redirect('notifications:notifications')