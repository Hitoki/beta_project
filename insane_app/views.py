from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from insane_app.models import Story, Product, Category


class StoryListView(ListView):

    model = Story
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class StoryDetailView(DetailView):

    model = Story

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ProductListView(ListView):

    model = Product
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["category_set"] = Category.objects.all().order_by('name')
        return context

    def get_queryset(self):
        categories_id = self.request.GET.getlist('categories')
        if categories_id:
            return self.model.objects.filter(categories__pk__in = categories_id)
        else:
            return self.model.objects.all()


class ProductDetailView(DetailView):

    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
