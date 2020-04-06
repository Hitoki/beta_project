from django.views.generic import ListView, DetailView
from .models import Product, News, Film, CinemaPerson

films_by_imdb = Film.objects.select_related("imdb_rating").values(
    "pk", "title", "imdb_rating__value"
).order_by("-imdb_rating__value")

top_films = Film.objects.values("pk", "title", "budget", "usa_gross")
films_by_budget = top_films.order_by("-budget")
films_by_usa_gross = top_films.order_by("-usa_gross")


class ProductListView(ListView):
    model = Product
    paginate_by = 8


class ProductDetailView(DetailView):
    model = Product


class FilmDetailView(DetailView):
    model = Film


class CinemaPersonDetailView(DetailView):
    model = CinemaPerson
    context_object_name = 'cinema_person'
    template_name = 'cinema/cinema_person_detail.html'


class NewsListView(ListView):
    model = News
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['films_by_imdb'] = films_by_imdb
        context['films_by_budget'] = films_by_budget
        context['films_by_usa_gross'] = films_by_usa_gross
        return context


class NewsDetailView(DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['films_by_imdb'] = films_by_imdb
        context['films_by_budget'] = films_by_budget
        context['films_by_usa_gross'] = films_by_usa_gross
        return context
