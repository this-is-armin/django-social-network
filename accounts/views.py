from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

from .models import CustomUser, Relation
from .forms import UserSignUpForm, UserSignInForm, UserEditForm


class UserSignUpView(View):
    template_name = 'accounts/signup.html'
    form_class = UserSignUpForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
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
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
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
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully signed out')
        return redirect('home:home')


class UserProfileView(View):
    template_name = 'accounts/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = get_object_or_404(CustomUser, username=kwargs['username'])
        is_followed = Relation.objects.filter(from_user=request.user, to_user=user).exists()

        context = {
            'user': user,
            'is_followed': is_followed,

            'delete_url': user.get_delete_url,
            'edit_url': user.get_edit_url,
            'signout_url': user.get_signout_url,
            'new_post_url': user.get_new_post_url,
            'follow_url': user.get_follow_url,
            'unfollow_url': user.get_unfollow_url,

            'posts_list_url': user.get_posts_list_url,
            'saved_posts_list_url': user.get_saved_posts_list_url,
            'liked_posts_list_url': user.get_liked_posts_list_url,
            'comments_list_url': user.get_comments_list_url,
            'comments_list_url': user.get_comments_list_url,
            'followers_list_url': user.get_followers_list_url,
            'following_list_url': user.get_followers_list_url,

            'posts_count': user.get_posts_count,
            'saved_posts_count': user.get_saved_posts_count,
            'liked_posts_count': user.get_liked_posts_count,
            'comments_count': user.get_comments_count,
            'followers_count': user.get_followers_count,
            'following_count': user.get_followers_count,
        }
        return render(request, self.template_name, context)


class UserDeleteView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(CustomUser, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        if request.user != self.user_instance:
            return redirect(request.META.get('HTTP_REFERER') or self.user_instance.get_profile_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        self.user_instance.delete()
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
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        if request.user != self.user_instance:
            return redirect(request.META.get('HTTP_REFERER') or self.user_instance.get_profile_url)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class(initial={
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'image': user.image,
        })
        context = {
            'user': user,
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = self.user_instance

        if form.is_valid():
            cd = form.cleaned_data

            if cd['username'] == user.username:
                user.email = cd['email']
                user.first_name = cd['first_name']
                user.last_name = cd['last_name']
                user.bio = cd['bio']
                
                if cd['image'] is not None:
                    user.image = cd['image']
                
                if request.POST.get('delete_profile_picture'):
                    user.image.delete()

                user.save()
                messages.success(request, 'Successfully edited account')
                return redirect(user.get_profile_url)
            else:
                if CustomUser.objects.filter(username=cd['username']).exists():
                    messages.error(request, 'This username already exists')
                    return redirect(user.get_edit_account_url)
                else:
                    user.username = cd['username']
                    user.email = cd['email']
                    user.first_name = cd['first_name']
                    user.last_name = cd['last_name']
                    user.bio = cd['bio']
                    
                    if cd['image'] is not None:
                        user.image = cd['image']
                    
                    if request.POST.get('delete_profile_picture'):
                        user.image.delete()

                    user.save()
                    messages.success(request, 'Successfully edited account')
                    return redirect(request.META.get('HTTP_REFERER') or user.get_profile_url)
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
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        if request.user == self.user_instance:
            return redirect(request.META.get('HTTP_REFERER') or self.user_instance.get_profile_url)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance

        if not Relation.objects.filter(from_user=request.user, to_user=user).exists():
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, f"Successfully followed '{user.username}'")
        return redirect(request.META.get('HTTP_REFERER') or  user.get_profile_url)


class UserUnfollowView(View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(CustomUser, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        if request.user == self.user_instance:
            return redirect(request.META.get('HTTP_REFERER') or self.user_instance.get_profile_url)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance

        if Relation.objects.filter(from_user=request.user, to_user=user).exists():
            Relation.objects.get(from_user=request.user, to_user=user).delete()
            messages.success(request, f"Successfully unfollowed '{user.username}'")
        return redirect(request.META.get('HTTP_REFERER') or user.get_profile_url)


class UserFollowersView(View):
    template_name = 'accounts/followers.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = get_object_or_404(CustomUser, username=kwargs['username'])
        context = {
            'followers_list': user.get_followers_list,
        }
        return render(request, self.template_name, context)


class UserFollowingView(View):
    template_name = 'accounts/following.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = get_object_or_404(CustomUser, username=kwargs['username'])
        context = {
            'user': user,
            'following_list': user.get_following_list,
        }
        return render(request, self.template_name, context)


class UserPostsView(View):
    template_name = 'accounts/posts.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = get_object_or_404(CustomUser, username=kwargs['username'])
        context = {
            'posts_list': user.get_posts_list,
        }
        return render(request, self.template_name, context)
    

class UserCommentsView(View):
    template_name = 'accounts/comments.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(CustomUser, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        if request.user != self.user_instance:
            return redirect(request.META.get('HTTP_REFERER') or self.user_instance.get_profile_url)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        context = {
            'comments_list': user.get_comments_list,
        }
        return render(request, self.template_name, context)


class UserSavedPostsView(View):
    template_name = 'accounts/saved-posts.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(CustomUser, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        if request.user != self.user_instance:
            return redirect(request.META.get('HTTP_REFERER') or self.user_instance.get_profile_url)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        context = {
            'saved_posts_list': self.user_instance.get_saved_posts_list,
        }
        return render(request, self.template_name, context)


class UserLikedPostsView(View):
    template_name = 'accounts/liked-posts.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(CustomUser, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        if request.user != self.user_instance:
            return redirect(request.META.get('HTTP_REFERER') or self.user_instance.get_profile_url)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        context = {
            'liked_posts_list': self.user_instance.get_liked_posts_list,
        }
        return render(request, self.template_name, context)