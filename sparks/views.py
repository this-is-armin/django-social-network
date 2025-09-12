from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Spark
from .forms import CommentForm, EditSparkForm

from utils.pagination import get_pagination_context


class SparksView(LoginRequiredMixin, View):
    template_name = 'sparks/sparks.html'

    def get(self, request):
        sparks = Spark.objects.all()

        if request.GET.get('search'):
            search = request.GET['search']
            sparks = sparks.filter(content__contains=search)

        return render(request, self.template_name, {
            'page_obj': get_pagination_context(request, sparks, 50),
        })


class SparkDetailView(LoginRequiredMixin, View):
    template_name = 'sparks/spark_detail.html'
    form_class = CommentForm

    def setup(self, request, *args, **kwargs):
        self.spark_instance = get_object_or_404(Spark, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, **kwargs):
        spark = self.spark_instance
        comments = spark.get_comments_list()
        return render(request, self.template_name, {
            'spark': spark,
            'comments': comments,
            'form': self.form_class(),
        })
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            spark = self.spark_instance
            comment = form.save(commit=False)
            comment.user = request.user
            comment.spark = spark
            comment.save()
            messages.success(request, 'Successfully sent a comment', 'info')
            return redirect(spark.get_absolute_url())
        spark = self.spark_instance
        comments = spark.get_comments_list()
        return render(request, self.template_name, {
            'spark': spark,
            'comments': comments,
            'form': form,
        })


class EditSparkView(LoginRequiredMixin, View):
    template_name = 'sparks/edit_spark.html'
    form_class = EditSparkForm

    def setup(self, request, *args, **kwargs):
        self.spark_instance = get_object_or_404(Spark, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, **kwargs):
        spark = self.spark_instance
        return render(request, self.template_name, {
            'spark': spark,
            'form': self.form_class(instance=spark),
        })
    
    def post(self, request, **kwargs):
        spark = self.spark_instance
        form = self.form_class(request.POST, instance=spark)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully edited spark', 'info')
            return redirect(spark.get_absolute_url())
        spark = self.spark_instance
        return render(request, self.template_name, {
            'spark': spark,
            'form': form,
        })


class DeleteSparkView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        spark = get_object_or_404(Spark, pk=kwargs['pk'])

        if spark.user == request.user:
            spark.delete()
            messages.success(request, 'Successfully deleted spark', 'info')
            return redirect(request.user.get_sparks_list_url())
        return redirect(spark.get_absolute_url())