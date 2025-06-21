from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator

from .models import CustomUser, Relation
from .forms import UserSignUpForm, UserSignInForm, UserEditForm


class UserSignUpView(View):
    template_name = 'accounts/signup.html'
    form_class = UserSignUpForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = CustomUser.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            messages.success(request, 'Successfully signed up')
            return redirect('accounts:signin')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class UserSignInView(View):
    template_name = 'accounts/signin.html'
    form_class = UserSignInForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully signed in')
                return redirect('home:home')
            messages.error(request, 'Username or Password is wrong')
            return redirect('accounts:signin')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class UserSignOutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully signed out')
        return redirect('home:home')


class UserProfileView(View):
    template_name = 'accounts/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = get_object_or_404(CustomUser, username=kwargs['username'])
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            is_followed = True
        else:
            is_followed = False

        context = {
            'user': user,
            'is_followed': is_followed,
        }
        return render(request, self.template_name, context)


class UserDeleteView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(CustomUser, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user != self.user_instance:
            return redirect('accounts:profile', self.user_instance)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        user.delete()
        messages.success(request, 'Successfully deleted account')
        return redirect('home:home')
    

class UserEditView(View):
    template_name = 'accounts/edit.html'
    form_class = UserEditForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(CustomUser, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user != self.user_instance:
            return redirect('accounts:profile', self.user_instance.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        INITIAL = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'bio': user.bio,
            'location': user.location,
            'image': user.image,
        }
        form = self.form_class(initial=INITIAL)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        old_user = self.user_instance

        if form.is_valid():
            cd = form.cleaned_data

            if cd['username'] == old_user.username:
                old_user.email = cd['email']
                old_user.first_name = cd['first_name']
                old_user.last_name = cd['last_name']
                old_user.age = cd['age']
                old_user.bio = cd['bio']
                old_user.location = cd['location']
                old_user.image = cd['image']
                old_user.save()
                messages.success(request, 'Successfully edited account')
                return redirect('accounts:profile', old_user.username)
            else:
                user = CustomUser.objects.filter(username=cd['username'])

                if user.exists():
                    messages.error(request, 'This username already exists')
                    return redirect(old_user.edit_account)
                else:
                    old_user.username = cd['username']
                    old_user.email = cd['email']
                    old_user.first_name = cd['first_name']
                    old_user.last_name = cd['last_name']
                    old_user.age = cd['age']
                    old_user.bio = cd['bio']
                    old_user.location = cd['location']
                    old_user.image = cd['image']
                    old_user.save()
                    messages.success(request, 'Successfully edited account')
                    return redirect('accounts:profile', old_user.username)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class UserFollowView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(CustomUser, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user == self.user_instance:
            return redirect('accounts:profile', self.user_instance.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if not relation.exists():
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, f"Successfully followed '{user.username}'")
        return redirect('accounts:profile', user.username)


class UserUnfollowView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(CustomUser, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user == self.user_instance:
            return redirect('accounts:profile', self.user_instance.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            Relation.objects.get(from_user=request.user, to_user=user).delete()
            messages.success(request, f"Successfully unfollowed '{user.username}'")
        return redirect('accounts:profile', user.username)


class UserFollowersView(View):
    template_name = 'accounts/followers.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = get_object_or_404(CustomUser, username=kwargs['username'])
        followers = user.followers.all()
        context = {
            'user': user,
            'followers': followers,
        }
        return render(request, self.template_name, context)


class UserFollowingView(View):
    template_name = 'accounts/following.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = get_object_or_404(CustomUser, username=kwargs['username'])
        following = user.following.all()
        context = {
            'user': user,
            'following': following,
        }
        return render(request, self.template_name, context)


class UserPostsView(View):
    template_name = 'accounts/posts.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = get_object_or_404(CustomUser, username=kwargs['username'])
        posts = user.posts.all()

        paginator = Paginator(posts, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'posts': posts,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)
    

class UserCommentsView(View):
    template_name = 'accounts/comments.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(CustomUser, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        if request.user != self.user_instance:
            return redirect('accounts:profile', self.user_instance.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        comments = user.comments.all()

        paginator = Paginator(comments, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'comments': comments,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)