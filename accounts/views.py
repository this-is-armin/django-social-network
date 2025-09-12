from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q

from .models import Relation
from .forms import RegisterForm, LoginForm, EditAccountForm, DeleteAccountForm, AddSparkForm

from utils.mixins import AnonymousRequiredMixin, OwnerRequiredMixin, SelfForbiddenMixin
from utils.pagination import get_pagination_context


User = get_user_model()


class PeopleView(LoginRequiredMixin, View):
    template_name = 'accounts/people.html'

    def get(self, request):
        users = User.objects.all()

        if request.GET.get('search'):
            search = request.GET['search']
            users = users.filter(
                Q(username__istartswith=search) |
                Q(first_name__istartswith=search) |
                Q(last_name__istartswith=search) |
                Q(email__istartswith=search) |
                Q(bio__icontains=search)
            )
            
        return render(request, self.template_name, {
            'page_obj': get_pagination_context(request, users, 50),
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
            messages.success(request, 'Successfully Registered', 'info')
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
                messages.success(request, 'Successfully Loged In', 'info')
                return redirect(request.GET.get('next') or 'base:social_network')
            messages.error(request, 'Incorrect Username or Password', 'danger')
            return redirect('accounts:login')
        return render(request, self.template_name, {
            'form': form,
        })


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully Loged Out', 'info')
        return redirect('base:social_network')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        is_followed = Relation.objects.filter(from_user=request.user, to_user=user).exists()
        return render(request, self.template_name, {
            'user': user,
            'is_followed': is_followed,
        })


class EditAccountView(LoginRequiredMixin, OwnerRequiredMixin, View):
    template_name = 'accounts/edit_account.html'
    form_class = EditAccountForm

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


class DeleteProfileImageView(LoginRequiredMixin, OwnerRequiredMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if user.image:
            user.image.delete()
            messages.success(request, 'Successfully deleted profile image', 'info')
        return redirect(user.get_edit_account_url())


class DeleteAccountView(LoginRequiredMixin, OwnerRequiredMixin, View):
    template_name = 'accounts/delete_account.html'
    form_class = DeleteAccountForm

    def get(self, request, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(),
        })
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = get_object_or_404(User, username=kwargs['username'])

            if cd['username'] == user.username:
                user.delete()
                messages.success(request, 'Successfully deleted account', 'info')
                return redirect('base:social_network')
            messages.error(request, 'Incorrect Username', 'danger')
            return redirect(user.get_delete_account_url())
        return render(request, self.template_name, {
            'form': form,
        })
    

class AddSparkView(LoginRequiredMixin, OwnerRequiredMixin, View):
    template_name = 'accounts/add_spark.html'
    form_class = AddSparkForm

    def get(self, request, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(),
        })
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = get_object_or_404(User, username=kwargs['username'])
            spark = form.save(commit=False)
            spark.user = user
            spark.save()
            messages.success(request, 'Successfully added a spark', 'info')
            return redirect(user.get_profile_url())
        return render(request, self.template_name, {
            'form': form,
        })


class SparksView(LoginRequiredMixin, View):
    template_name = 'accounts/sparks.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        sparks = user.get_sparks_list()

        if request.GET.get('search'):
            search = request.GET['search']
            sparks = sparks.filter(content__contains=search)

        return render(request, self.template_name, {
            'user': user,
            'page_obj': get_pagination_context(request, sparks, 50),
        })


class FollowView(LoginRequiredMixin, SelfForbiddenMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if not Relation.objects.filter(from_user=request.user, to_user=user).exists():
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, f"Successfully followed {user.username}", 'info')
        return redirect(user.get_profile_url())


class UnfollowView(LoginRequiredMixin, SelfForbiddenMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            relation.delete()
            messages.success(request, f"Successfully unfollowed {user.username}", 'info')
        return redirect(user.get_profile_url())


class FollowersListView(LoginRequiredMixin, View):
    template_name = 'accounts/followers_list.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        followers_list = user.get_followers_list()

        if request.GET.get('search'):
            search = request.GET['search']
            followers_list = followers_list.filter(
                Q(username__istartswith=search) |
                Q(first_name__istartswith=search) |
                Q(last_name__istartswith=search) |
                Q(email__istartswith=search) |
                Q(bio__icontains=search)
            )

        return render(request, self.template_name, {
            'user': user,
            'page_obj': get_pagination_context(request, followers_list, 50),
        })


class FollowingListView(LoginRequiredMixin, View):
    template_name = 'accounts/following_list.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        following_list = user.get_following_list()
        
        if request.GET.get('search'):
            search = request.GET['search']
            following_list = following_list.filter(
                Q(username__istartswith=search) |
                Q(first_name__istartswith=search) |
                Q(last_name__istartswith=search) |
                Q(email__istartswith=search) |
                Q(bio__icontains=search)
            )
        
        return render(request, self.template_name, {
            'user': user,
            'page_obj': get_pagination_context(request, following_list, 50),
        })