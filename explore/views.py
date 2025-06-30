from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages

from .forms import NewPostForm
from .models import Post, Comment, PostSave, PostLike


class ExploreView(View):
    template_name = 'explore/explore.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        posts_list = Post.objects.all()

        if request.GET.get('search'):
            posts_list = posts_list.filter(description__contains=request.GET['search'])

        paginator = Paginator(posts_list, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class PostView(View):
    template_name = 'explore/post.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        post = self.post_instance
        is_saved = PostSave.objects.filter(post=post, user=request.user).exists()
        is_liked = PostLike.objects.filter(post=post, user=request.user).exists()

        context = {
            'post': post,
            'is_saved': is_saved,
            'is_liked': is_liked,

            'save_url': post.get_save_url,
            'unsave_url': post.get_unsave_url,
            'like_url': post.get_like_url,
            'unlike_url': post.get_unlike_url,

            'likes_count': post.get_likes_count,
            'comments_list': post.get_comments_list,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        post = self.post_instance
        body = request.POST.get('body')

        Comment.objects.create(post=post, user=request.user, body=body)
        messages.success(request, 'Successfully sent comment')
        return redirect(post.get_absolute_url)


class PostDeleteView(View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        if request.user != self.post_instance.user:
            return redirect(request.META.get('HTTP_REFERER') or 'explore:explore')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        self.post_instance.delete()
        messages.success(request, 'Successfully deleted post')
        return redirect(request.META.get('HTTP_REFERER') or request.user.get_posts_list_url)


class CommentDeleteView(View):
    def setup(self, request, *args, **kwargs):
        self.comment_instance = get_object_or_404(Comment, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        if request.user != self.comment_instance.user:
            return redirect(request.META.get('HTTP_REFERER') or 'explore:explore')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        self.comment_instance.delete()
        messages.success(request, 'Successfully deleted comment')
        return redirect(request.META.get('HTTP_REFERER') or request.user.get_comments_list_url)


class NewPostView(View):
    template_name = 'explore/new-post.html'
    form_class = NewPostForm    

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
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
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Successfully added post')
            return redirect(request.user.get_profile_url)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class PostEditView(View):
    template_name = 'explore/post-edit.html'
    form_class = NewPostForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post,pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        if request.user != self.post_instance.user:
            return redirect('explore:explore')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Successfully edited post')
            return redirect(request.user.get_profile_url)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class PostSaveView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])

        if not PostSave.objects.filter(post=post, user=request.user).exists():
            PostSave.objects.create(post=post, user=request.user)
            messages.success(request, 'Successfully saved post')
        return redirect(request.META.get('HTTP_REFERER') or post.get_absolute_url)


class PostUnSaveView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])

        if PostSave.objects.filter(post=post, user=request.user).exists():
            PostSave.objects.get(post=post, user=request.user).delete()
            messages.success(request, 'Successfully unsaved post')
        return redirect(request.META.get('HTTP_REFERER') or post.get_absolute_url)


class PostLikeView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])

        if not PostLike.objects.filter(post=post, user=request.user).exists():
            PostLike.objects.create(post=post, user=request.user)
            messages.success(request, 'Successfully liked post')
        return redirect(request.META.get('HTTP_REFERER') or post.get_absolute_url)


class PostUnLikeView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER') or 'home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])

        if PostLike.objects.filter(post=post, user=request.user).exists():
            PostLike.objects.get(post=post, user=request.user).delete()
            messages.success(request, 'Successfully unliked post')
        return redirect(request.META.get('HTTP_REFERER') or post.get_absolute_url)