from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages

from .models import Comment, Like, Post, PostSave
from .forms import PostCreateUpdateForm, CommentSendForm, PostSearchForm


page_urls = {
    'home' : 'base:home'
}

def home_view(request):
    return render(request, 'base/index.html')


class PostsView(View):
    template_name = 'posts/posts.html'
    form_class = PostSearchForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        posts = Post.objects.all()
        form = self.form_class()

        if request.GET.get('search_text'):
            search_text = request.GET.get('search_text')
            posts = posts.filter(title__contains = search_text)
        return render(request, self.template_name, {'posts':posts, 'form':form})


class PostDetailView(View):
    template_name = 'posts/detail.html'
    form_class = CommentSendForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        comments = post.comments.all()
        form = self.form_class()
        like_exists = Like.objects.filter(post=post, user=request.user).exists()
        save_exists = PostSave.objects.filter(user=request.user, post=post).exists()

        if like_exists: can_like = False
        else: can_like = True

        if save_exists: can_save = False
        else: can_save = True

        return render(request, self.template_name, {'post':post, 'can_like':can_like, 'can_save':can_save, 'comments':comments, 'form':form})

    def post(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            Comment.objects.create(user=request.user, post=post, body=cd['body']).save()
            messages.success(request, 'The comment was sent', 'success')
            return redirect(post.post_detail())
        return render(request, self.template_name, {'post':post, 'form':form})


class PostCreateView(View):
    template_name = 'posts/create.html'
    form_class = PostCreateUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            Post.objects.create(user=request.user, title=cd['title'], description=cd['description'], body=cd['body']).save()
            messages.success(request, 'The post was created', 'success')
            return redirect('account:user_profile', request.user)
        return render(request, self.template_name, {'form':form})


def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.user.is_authenticated: return redirect(page_urls['home'])
    if request.user != post.user:  return redirect(post.post_detail())
    post.delete()
    messages.success(request, 'The post was deleted', 'success')
    return redirect('account:user_posts', request.user)


class PostLikeView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        like_exists = post.likes.filter(user=request.user, post=post).exists()

        if not like_exists:
            Like.objects.create(user=request.user, post=post).save()
            messages.success(request, 'The post was liked', 'success')
        return redirect(post.post_detail())


class PostUpdateView(View):
    template_name = 'posts/update.html'
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(page_urls['home'])
        if request.user != self.post_instance.user: return redirect(self.post_instance.post_detail())
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = self.post_instance
        INITIAL = {'title':post.title, 'description':post.description, 'body':post.body}
        form = self.form_class(initial=INITIAL)
        return render(request, self.template_name, {'form':form})

    def post(self, request, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post.title = cd['title']
            post.description = cd['description']
            post.body = cd['body']
            post.save()
            messages.success(request, "The post was updated", 'success')
            return redirect('account:user_posts', request.user)
        return render(request, self.template_name, {'form':form})


class PostSaveView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        save_exists = post.saves.filter(user=request.user).exists()

        if not save_exists:
            PostSave.objects.create(user=request.user, post=post).save()
            messages.success(request, 'The post was saved', 'success')
        return redirect(post.post_detail())


class PostUnSaveView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(page_urls['home'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        save_exists = post.saves.filter(user=request.user)

        if save_exists.exists():
            save_exists.delete()
            messages.success(request, 'The post was un-saved', 'success')
        return redirect(post.post_detail())


def post_comment_delete(request, **kwargs):
    post = get_object_or_404(Post, pk=kwargs['pk'])
    comment = post.comments.get(pk=kwargs['comment_pk'])
    if not request.user.is_authenticated: return redirect(page_urls['home'])
    if request.user != post.user: return redirect(post.post_detail())
    comment.delete(); messages.success(request, 'The comment was deleted', 'success')
    return redirect(post.post_detail())
