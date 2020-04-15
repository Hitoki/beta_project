from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, News, Film, CinemaPerson, MpaaRating

all_films = Film.objects.prefetch_related(
    "staff__cinemafilmpersonprofession_set__profession", "staff__user",
    "country", "genre", "language", "distributor", "news_set"
).select_related("imdb_rating", "mpaa_rating", "product")

top_films = all_films.values_list(
    "pk", "title", "imdb_rating__value", "budget", "usa_gross",
    "world_gross", named=True
)
imdb_top_5 = top_films.order_by("-imdb_rating__value")[:5]
budget_top_5 = top_films.order_by("-budget")[:5]
usa_gross_top_5 = top_films.order_by("-usa_gross")[:5]
world_gross_top_5 = top_films.order_by("-world_gross")[:5]

professions = ("Director", "Actor", "Writer")
persons_by_films = {}

for film in all_films:
    persons_by_films[film.pk] = {}

    for profession in professions:
        persons_by_films[film.pk][profession] = []
        film_persons = film.staff.filter(
            cinemafilmpersonprofession__profession__name=profession
        ).order_by("pk").values_list(
            "pk", "user__first_name", "user__last_name", named=True
        )
        for person in film_persons:
            persons_by_films[film.pk][profession].append(
                {"pk": person.pk,
                 "name": f"{person.user__first_name} "
                         f"{person.user__last_name}"}
            )
film_fields = (
    "country__name", "genre__name", "language__name",
    "distributor__name", "news__pk", "news__title"
)
info_by_films_qs = all_films.values_list(
    "pk", *film_fields, named=True
).order_by("-news__created_at")

info_by_films = {}
for film in info_by_films_qs:
    if film.pk not in info_by_films:
        info_by_films[film.pk] = {}

    for field in film_fields:
        if field not in ("news__pk", "news__title"):
            if field not in info_by_films[film.pk]:
                info_by_films[film.pk][field] = []
            if field == "country__name" and film.country__name not in \
                    info_by_films[film.pk][field]:
                info_by_films[film.pk][field].append(film.country__name)
            elif field == "genre__name" and film.genre__name not in \
                    info_by_films[film.pk][field]:
                info_by_films[film.pk][field].append(film.genre__name)
            elif field == "language__name" and film.language__name not in \
                    info_by_films[film.pk][field]:
                info_by_films[film.pk][field].append(film.language__name)
            elif field == "distributor__name" and film.distributor__name \
                    not in info_by_films[film.pk][field]:
                info_by_films[film.pk][field].append(film.distributor__name)
        else:
            if "news" not in info_by_films[film.pk]:
                info_by_films[film.pk]["news"] = {}
            if field == "news__pk" and film.news__pk and film.news__pk not in \
                    info_by_films[film.pk]["news"]:
                info_by_films[film.pk]["news"][film.news__pk] = film.news__title

all_persons = CinemaPerson.objects.prefetch_related(
    "film_set__genre", "film_set__imdb_rating", "news_set"
).select_related("user")


class ProductListView(ListView):
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.select_related("film").only(
            "pk", "price", "film"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Movies on Blu-ray'
        context['persons_by_films'] = persons_by_films
        return context


class TopRatedProductListView(ProductListView):

    def get_queryset(self):
        return super().get_queryset().order_by("-film__imdb_rating__value")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Top Rated Movies on Blu-ray'
        return context


class NewReleasesProductListView(ProductListView):

    def get_queryset(self):
        return super().get_queryset().order_by("-film__release_data")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'New Releases Movies on Blu-ray'
        return context


class IndexListView(ListView):
    template_name = 'cinema/index_list.html'
    context_object_name = 'new_releases_list'

    queryset = Product.objects.select_related("film").only(
        "pk", "price", "film"
    ).order_by("-film__imdb_rating__value")

    def get_queryset(self):
        return self.queryset.order_by("-film__release_data")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_list = News.objects.only(
            "pk", "title", "news_source", "news_detail_photo", "created_at"
        )
        context['page_title'] = "Latest Movie News, Movies on Blu-ray"
        context['title_news'] = "Cinema News"
        context['description_news'] = "The latest movie news on the movies " \
                                      "'you're most interested in seeing. "
        context['title_blu_ray'] = "Movies on Blu-ray"
        context['description_blu_ray'] = "Welcome to the fantastic Blu-ray " \
                                         "department here, where you can find " \
                                         "the films, you could ever want to " \
                                         "see in superb high definition " \
                                         "quality. We're constantly adding " \
                                         "all of the latest Blu-ray releases " \
                                         "to our collection and always have " \
                                         "an unbelievable offer or two. We " \
                                         "promise great deals on the best " \
                                         "films! "
        context['title_top_rated'] = 'Top Rated'
        context['title_new_releases'] = 'New Releases'
        context['persons_by_films'] = persons_by_films
        context['news_list'] = news_list
        context['top_rated_list'] = self.queryset

        return context


class ProductDetailView(DetailView):

    def get_queryset(self):
        return Product.objects.select_related(
            "film__imdb_rating", "film__mpaa_rating"
        ).filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film_info = info_by_films[self.kwargs.get('pk')]
        context['countries'] = sorted(film_info['country__name'])
        context['genres'] = sorted(film_info['genre__name'])
        context['languages'] = sorted(film_info['language__name'])
        context['distributors'] = sorted(film_info['distributor__name'])
        context['film_persons'] = persons_by_films[self.kwargs.get('pk')]

        return context


class FilmListView(ListView):
    paginate_by = 8

    def get_queryset(self):
        return Film.objects.select_related("imdb_rating", "mpaa_rating")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Movies [A-Z]'
        context['info_by_films'] = info_by_films
        context['persons_by_films'] = persons_by_films
        return context


class TopRatedFilmListView(FilmListView):

    def get_queryset(self):
        return super().get_queryset().order_by("-imdb_rating__value")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Top Rated IMDb Movies'
        context['criterion_name'] = 'IMDb Rating'
        return context


class BudgetFilmListView(FilmListView):

    def get_queryset(self):
        return super().get_queryset().order_by("-budget")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Most Expensive Movies'
        context['criterion_name'] = 'Budget'
        return context


class UsaGrossFilmListView(FilmListView):

    def get_queryset(self):
        return super().get_queryset().order_by("-usa_gross")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Most USA Grossing Movies'
        context['criterion_name'] = 'USA Gross'
        return context


class WorldGrossFilmListView(FilmListView):

    def get_queryset(self):
        return super().get_queryset().order_by("-world_gross")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Most Worldwide Grossing Movies'
        context['criterion_name'] = 'World Gross'
        return context


class YearFilmListView(FilmListView):

    def get_queryset(self):
        self.requested_year = self.kwargs.get('year')
        return super().get_queryset().filter(
            release_data__year=self.requested_year
        ).order_by("-imdb_rating__value")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular Movies of {self.requested_year}'
        return context


class GenreFilmListView(FilmListView):

    def get_queryset(self):
        self.requested_genre = self.kwargs.get('genre')
        return super().get_queryset().filter(
            genre__name=self.requested_genre
        ).order_by("-imdb_rating__value")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular {self.requested_genre} Movies'
        return context


class CountryFilmListView(FilmListView):

    def get_queryset(self):
        self.requested_country = self.kwargs.get('country')
        return super().get_queryset().filter(
            country__name=self.requested_country
        ).order_by("-imdb_rating__value")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular {self.requested_country} Movies'
        return context


class LanguageFilmListView(FilmListView):

    def get_queryset(self):
        self.requested_language = self.kwargs.get('language')
        return super().get_queryset().filter(
            language__name=self.requested_language
        ).order_by("-imdb_rating__value")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            'page_title'] = f'Most Popular Movies in {self.requested_language}'
        return context


class DistributorFilmListView(FilmListView):

    def get_queryset(self):
        self.requested_distributor = self.kwargs.get('distributor')
        return super().get_queryset().filter(
            distributor__name=self.requested_distributor
        ).order_by("-imdb_rating__value")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Most Popular Movies of " \
                                f"{self.requested_distributor}"
        return context


class MpaaFilmListView(FilmListView):

    def get_queryset(self):
        self.requested_mpaa = self.kwargs.get('pk')
        return super().get_queryset().filter(
            mpaa_rating__pk=self.requested_mpaa
        ).order_by("-imdb_rating__value")

    def get_context_data(self, **kwargs):
        mpaa = MpaaRating.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular Movies with MPAA Rating of ' \
                                f'{mpaa.value}'
        context['page_description'] = mpaa.description
        return context


class FilmDetailView(DetailView):

    def get_queryset(self):
        return Film.objects.select_related(
            "imdb_rating", "mpaa_rating"
        ).filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film_info = info_by_films[self.kwargs.get('pk')]
        context['countries'] = sorted(film_info['country__name'])
        context['genres'] = sorted(film_info['genre__name'])
        context['languages'] = sorted(film_info['language__name'])
        context['distributors'] = sorted(film_info['distributor__name'])
        context['related_news'] = film_info['news']
        context['film_persons'] = persons_by_films[self.kwargs.get('pk')]

        return context


class CinemaPersonDetailView(DetailView):
    context_object_name = 'cinema_person'
    template_name = 'cinema/cinema_person_detail.html'

    person_fields = ("film__genre__name", "news__pk")
    info_by_persons_qs = all_persons.values_list(
        "pk", *person_fields, "news__title", named=True
    ).order_by("-news__created_at")

    info_by_persons = {}
    for person in info_by_persons_qs:
        if person.pk not in info_by_persons:
            info_by_persons[person.pk] = {}

        for field in person_fields:
            if "news" not in info_by_persons[person.pk]:
                info_by_persons[person.pk]["news"] = {}
            if field == "film__genre__name":
                if field not in info_by_persons[person.pk]:
                    info_by_persons[person.pk][field] = []
                if person.film__genre__name not in info_by_persons[
                        person.pk][field]:
                    info_by_persons[person.pk][field].append(
                        person.film__genre__name
                    )
            elif field == "news__pk" and person.news__pk and person.news__pk \
                    not in info_by_persons[person.pk]["news"]:
                info_by_persons[person.pk]["news"][
                    person.news__pk] = person.news__title

    def get_queryset(self):
        return CinemaPerson.objects.select_related("user", "country").filter(
            pk=self.kwargs.get('pk')
        )

    def get_context_data(self, **kwargs):
        person_extra_info = self.info_by_persons[self.kwargs.get('pk')]

        person_info = CinemaPerson.objects.get(pk=self.kwargs.get('pk'))
        person_professions = sorted(
            set(
                person_info.cinemafilmpersonprofession_set.values_list(
                    "profession__name", flat=True
                )
            )
        )
        filmography = {}
        for person_profession in person_professions:
            film_info_qs = person_info.film_set.filter(
                cinemafilmpersonprofession__profession__name=person_profession
            ).values_list(
                "pk", "title", "release_data__year", "imdb_rating__value",
                named=True
            ).order_by("-release_data")

            filmography[person_profession] = film_info_qs

        number_of_films = []
        years_of_films = []

        for person_films in filmography.values():
            for person_film in person_films:
                number_of_films.append(person_film.pk)
                years_of_films.append(person_film.release_data__year)

        context = super().get_context_data(**kwargs)
        context['genres'] = sorted(person_extra_info['film__genre__name'])
        context['related_news'] = person_extra_info['news']
        context['person_professions'] = tuple(person_professions)
        context['number_of_films'] = len(set(number_of_films))
        context['years_of_films'] = f'{min(years_of_films)} - ' \
                                    f'{max(years_of_films)}'
        context['filmography'] = filmography

        return context


class NewsListView(ListView):
    model = News
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Latest Movie News'
        context['imdb_top_5'] = imdb_top_5
        context['budget_top_5'] = budget_top_5
        context['usa_gross_top_5'] = usa_gross_top_5
        context['world_gross_top_5'] = world_gross_top_5
        return context


class CelebrityNewsListView(NewsListView):
    persons = CinemaPerson.objects.select_related("user").values_list(
        "user__first_name", "user__last_name", named=True
    )
    celebrities = [
        f"{person.user__first_name} {person.user__last_name}" for person in
        persons
    ]
    all_news = News.objects.values_list("pk", "title", named=True)
    news_titles = {news.pk: news.title for news in all_news}
    found_titles = []

    for pk, title in news_titles.items():
        for celebrity in celebrities:
            if celebrity in title:
                found_titles.append(pk)
                break

    def get_queryset(self):
        return super().get_queryset().filter(pk__in=self.found_titles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Latest Celebrity News'
        return context


class NewsDetailView(DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imdb_top_5'] = imdb_top_5
        context['budget_top_5'] = budget_top_5
        context['usa_gross_top_5'] = usa_gross_top_5
        context['world_gross_top_5'] = world_gross_top_5
        return context


class SearchResultsView(TemplateView):
    template_name = 'cinema/search_results.html'

    def get_context_data(self, **kwargs):
        context = {}
        query = self.request.GET.get('q')
        formatted_query = ' '.join(query.strip().split())

        if formatted_query:
            product_list = Product.objects.filter(
                film__title__icontains=formatted_query
            ).select_related('film')
            film_list = Film.objects.filter(title__icontains=formatted_query)
            query_fullname = formatted_query.split()
            person_list = CinemaPerson.objects.filter(
                Q(user__first_name__iexact=query_fullname[:1]) & Q(
                    user__last_name__iexact=query_fullname[1:]
                ) | Q(user__first_name__icontains=formatted_query) | Q(
                    user__last_name__icontains=formatted_query
                )
            ).select_related('user')
            news_list = News.objects.filter(title__icontains=formatted_query)
            context['product_list'] = product_list
            context['film_list'] = film_list
            context['person_list'] = person_list
            context['news_list'] = news_list

        context['search_title'] = 'Search results for '
        context['no_results'] = 'No results found for '
        context['query'] = query
        context['imdb_top_5'] = imdb_top_5
        context['budget_top_5'] = budget_top_5
        context['usa_gross_top_5'] = usa_gross_top_5
        context['world_gross_top_5'] = world_gross_top_5

        return context
