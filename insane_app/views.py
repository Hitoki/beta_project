from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

from insane_app.models import Story, Product, Category, StoryLike


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

        try:
            StoryLike.objects.get(story__pk = kwargs['object'].pk, user = User.objects.first())    #self.request.user)
            context['liked'] = True
        except StoryLike.DoesNotExist:
            pass

        return context


def like_story(request, pk):
    object, created = StoryLike.objects.get_or_create(
        user=User.objects.first(),
        story=Story.objects.get(pk=pk)
    )

    if not created:
        object.delete()
    else:
        created = 1

    return HttpResponse(created)


class StoryCreateView(CreateView):
    model = Story
    fields = ('name', 'body')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        
        return redirect(self.get_success_url())


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


class ProductCreateView(CreateView):

    model = Product
    fields = ('name', 'description', 'price')

    success_url = '/insane/market/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_set'] = Category.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        categories = self.request.POST.getlist('categories', ())
        self.object.save()

        if categories:
            self.object.categories.set(Category.objects.filter(pk__in=categories))
        return redirect(self.get_success_url())
