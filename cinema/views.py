from django.views.generic import TemplateView


class CinemaTemplateView(TemplateView):
    template_name = 'cinema/index.html'


class ProductDetailTemplateView(TemplateView):
    template_name = 'cinema/product_detail.html'


class NewsListTemplateView(TemplateView):
    template_name = 'cinema/news_list.html'


class NewsDetailTemplateView(TemplateView):
    template_name = 'cinema/news_detail.html'
