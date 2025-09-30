from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q

from .models import Relation
from .forms import (
    RegisterForm,
    LoginForm,
    AccountEditForm,
)

from utils.mixins import (
    AnonymousRequiredMixin,
    OwnerRequiredMixin,
    SelfForbiddenMixin,
)
from utils.pagination import get_pagination_context

from notifications.models import Notification


User = get_user_model()


class PeopleView(LoginRequiredMixin, View):
    template_name = 'accounts/people.html'

    def get(self, request):
        users = User.objects.all()

        if request.GET.get('search'):
            search = request.GET['search']
            users = users.filter(
                Q(username__contains=search) |
                Q(email__contains=search) |
                Q(first_name__contains=search) |
                Q(last_name__contains=search) |
                Q(bio__contains=search)
            )

        return render(request, self.template_name, {
            'page_obj': get_pagination_context(request, users, 10),
        })


class RegisterView(AnonymousRequiredMixin, View):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def get(self, request):
        return render(request, self.template_name, {
            'form': self.form_class(),
        })
    
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            messages.success(request, 'Successfully registered', 'info')
            return redirect('accounts:login')
        return render(request, self.template_name, {
            'form': form,
        })


class LoginView(AnonymousRequiredMixin, View):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get(self, request):
        return render(request, self.template_name, {
            'form': self.form_class(),
        })
    
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in', 'info')
                return redirect(request.GET.get('next') or 'social_network')
            messages.error(request, 'Incorrect Username or Password', 'danger')
            return redirect('accounts:login')
        return render(request, self.template_name, {
            'form': form,
        })


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully logged out', 'info')
        return redirect('social_network')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        is_followed = Relation.objects.filter(from_user=request.user, to_user=user).exists()
        return render(request, self.template_name, {
            'user': user,
            'is_followed': is_followed,
        })


class AccountEditView(LoginRequiredMixin, OwnerRequiredMixin, View):
    template_name = 'accounts/account_edit.html'
    form_class = AccountEditForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        return render(request, self.template_name, {
            'form': self.form_class(initial={
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'bio': user.bio,
            }),
        })
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            cd = form.cleaned_data
            user = self.user_instance

            if User.objects.filter(username=cd['username']).exclude(username=user.username).exists():
                form.add_error('username', 'This username already exists')
            else:
                user.username = cd['username']
                user.email = cd['email']
                user.first_name = cd['first_name']
                user.last_name = cd['last_name']
                user.bio = cd['bio']

                if cd['image'] is not None:
                    user.image = cd['image']

                user.save()
                messages.success(request, 'Successfully edited account', 'info')
                return redirect(user.get_profile_url())
            return render(request, self.template_name, {
                'form': form,
            })


class ProfileImageDeleteView(LoginRequiredMixin, OwnerRequiredMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if user.image:
            user.image.delete()
            messages.success(request, 'Successfully deleted profile image', 'info')
        return redirect(user.get_profile_url())


class AccountDeleteView(LoginRequiredMixin, OwnerRequiredMixin, View):
    def get(self, request, **kwargs):
        get_object_or_404(User, username=kwargs['username']).delete()
        messages.success(request, 'Successfully deleted account', 'info')
        return redirect('social_network')


class FollowView(LoginRequiredMixin, SelfForbiddenMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if not Relation.objects.filter(from_user=request.user, to_user=user).exists():
            relation = Relation.objects.create(from_user=request.user, to_user=user)
            Notification.objects.create(
                from_user=request.user,
                to_user=user,
                notification_type='follow',
                relation=relation,
            )
            messages.success(request, f"Successfully followed `{user.username}`", 'info')
        return redirect(user.get_profile_url())


class UnfollowView(LoginRequiredMixin, SelfForbiddenMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        
        if relation.exists():
            relation.delete()
            messages.success(request, f"Successfully unfollowed `{user.username}`", 'info')
        return redirect(user.get_profile_url())


class FollowersView(LoginRequiredMixin, View):
    template_name = 'accounts/followers.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        followers = user.get_followers()
        return render(request, self.template_name, {
            'user': user,
            'page_obj': get_pagination_context(request, followers, 10),
        })


class FollowingView(LoginRequiredMixin, View):
    template_name = 'accounts/following.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        following = user.get_following()
        return render(request, self.template_name, {
            'user': user,
            'page_obj': get_pagination_context(request, following, 10),
        })


class PostsView(LoginRequiredMixin, View):
    template_name = 'accounts/posts.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        posts = user.posts.all()
        return render(request, self.template_name, {
            'user': user,
            'page_obj': get_pagination_context(request, posts, 10),
        })