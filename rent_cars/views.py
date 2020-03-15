from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class AutoView(TemplateView):
    template_name = "auto.html"


class FeedView(TemplateView):
    template_name = "feed.html"


class PostView(TemplateView):
    template_name = "post.html"