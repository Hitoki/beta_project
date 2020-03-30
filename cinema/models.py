from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
)


def upload_to_film(instance, filename):
    return "films/{}_{}.jpg".format(instance.title, instance.pk)


def upload_to_cinema_person(instance, filename):
    return "cinema_persons/{}_{}_{}.jpg".format(
        instance.user.first_name, instance.user.last_name, instance.pk
    )


def upload_photo_to_news_feed(instance, filename):
    return "cinema_news_feed/{}_{}.jpg".format(instance.title, instance.pk)


def upload_photo_to_news_detail(instance, filename):
    return "cinema_news_detail/{}_{}.jpg".format(instance.title, instance.pk)


class ExtendedProfileMixin(models.Model):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    country = models.ForeignKey(
        "Country", on_delete=models.SET_NULL, blank=True, null=True
    )
    birthday = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_created=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "countries"
        ordering = ["name"]


class Genre(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ImdbRating(models.Model):
    value = models.DecimalField(max_digits=2, decimal_places=1, unique=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        ordering = ["value"]


class MpaaRating(models.Model):
    value = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=512, unique=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        ordering = ["value"]


class Language(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Distributor(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class CinemaPerson(ExtendedProfileMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(unique=True)
    oscar_awards = models.PositiveSmallIntegerField(default=0)
    avatar = models.ImageField(upload_to=upload_to_cinema_person, blank=True,
                               null=True)

    @property
    def age(self):
        if self.birthday:
            return (date.today() - self.birthday) // timedelta(days=365.2425)
        return None

    @property
    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def professions(self):
        professions = set(self.cinemafilmpersonprofession_set.select_related(
            "profession").values_list("profession__name", flat=True)
        )
        return sorted(professions)

    @property
    def filmography(self):
        filmography = {}

        for profession in self.professions:
            film_info = (self.film_set.filter(
                cinemafilmpersonprofession__profession__name=profession
            ).select_related("cinemafilmpersonprofession__profession"
                             ).values_list("pk", "title", "release_data__year",
                                           "imdb_rating__value", named=True
                                           ).order_by("-release_data"))
            filmography[profession] = film_info

        return filmography

    @property
    def genres(self):
        genres = set(self.film_set.prefetch_related("genre").values_list(
            "genre__name", flat=True)
        )
        return sorted(genres)

    @property
    def year_range(self):
        years = set(self.film_set.values_list("release_data__year", flat=True))
        return f"{min(years)} - {max(years)}"

    @property
    def related_news(self):
        return self.news_set.values_list("pk", "title", named=True)

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ["user__first_name"]


class Film(models.Model):
    title = models.CharField(max_length=64)
    country = models.ManyToManyField(Country)
    genre = models.ManyToManyField(Genre)
    staff = models.ManyToManyField(CinemaPerson,
                                   through="CinemaFilmPersonProfession")
    budget = models.PositiveIntegerField(null=True, blank=True)
    usa_gross = models.BigIntegerField(default=0)
    world_gross = models.BigIntegerField(default=0)
    run_time = models.DurationField()
    description = models.TextField(unique=True)
    release_data = models.DateField()
    language = models.ManyToManyField(Language)
    distributor = models.ManyToManyField(Distributor)
    imdb_rating = models.ForeignKey(
        ImdbRating, on_delete=models.SET_NULL, blank=True, null=True
    )
    mpaa_rating = models.ForeignKey(
        MpaaRating, on_delete=models.SET_NULL, blank=True, null=True
    )
    oscar_awards = models.PositiveSmallIntegerField(default=0)
    poster = models.ImageField(upload_to=upload_to_film, blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def year(self):
        return self.release_data.year

    @property
    def actors(self):
        qs = self.staff.filter(
            cinemafilmpersonprofession__profession__name="Actor"
        ).select_related("cinemafilmpersonprofession__profession"
                         ).values_list("pk", "user__first_name",
                                       "user__last_name", named=True
                                       ).order_by("pk")
        return qs

    @property
    def directors(self):
        qs = self.staff.filter(
            cinemafilmpersonprofession__profession__name="Director"
        ).select_related("cinemafilmpersonprofession__profession"
                         ).values_list("pk", "user__first_name",
                                       "user__last_name", named=True
                                       ).order_by("pk")
        return qs

    @property
    def writers(self):
        qs = self.staff.filter(
            cinemafilmpersonprofession__profession__name="Writer"
        ).select_related("cinemafilmpersonprofession__profession"
                         ).values_list("pk", "user__first_name",
                                       "user__last_name", named=True
                                       ).order_by("pk")
        return qs

    @property
    def related_news(self):
        return self.news_set.values_list("pk", "title", named=True)

    class Meta:
        ordering = ["-imdb_rating__value", "title"]


class CinemaProfession(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class CinemaFilmPersonProfession(models.Model):
    cinema_person = models.ForeignKey(CinemaPerson, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    profession = models.ForeignKey(CinemaProfession, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.film.title}: {self.profession.name} - "
            f"{self.cinema_person.fullname}"
        )

    class Meta:
        verbose_name = "cinema film person profession"
        verbose_name_plural = "Cinema films persons professions"
        ordering = ["film__title", "profession",
                    "cinema_person__user__first_name"]


class News(DateMixin):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(unique=True)
    news_source = models.CharField(max_length=32)
    news_author = models.CharField(max_length=64, default="", blank=True)
    film = models.ManyToManyField(Film, blank=True)
    cinema_person = models.ManyToManyField(CinemaPerson, blank=True)
    news_feed_photo = models.ImageField(
        upload_to=upload_photo_to_news_feed, blank=True, null=True
    )
    news_detail_photo = models.ImageField(
        upload_to=upload_photo_to_news_detail, blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "news"
        ordering = ["-created_at"]


class Product(DateMixin):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    in_stock = models.PositiveSmallIntegerField(default=0)
    film = models.OneToOneField(Film, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.film.title} [Blu-ray]"

    class Meta:
        ordering = ["-film__release_data"]


# class City(models.Model):
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     name = models.CharField(max_length=32, unique=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Address(models.Model):
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
#     region = models.CharField(max_length=32, default="", blank=True)
#     address_line1 = models.CharField(max_length=128, default="", blank=True)
#     address_line2 = models.CharField(max_length=128, default="", blank=True)
#     postal_code = models.CharField(max_length=5, default="", blank=True)
#     phone = models.CharField(max_length=16, default="", blank=True)
#
#     def __str__(self):
#         return f"{self.city.country.name} {self.city.name} {self.region} " \
#                f"{self.address_line1} {self.address_line2}"
#
#
# class Order(models.Model):
#     # order_date = models.DateTimeField(default=datetime.now)
#     order_details = models.ManyToManyField(Product, through='OrderDetails')
#     customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"{self.customer.__str__} order from {self.order_date}"
#
#
# class OrderDetails(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     quantity = models.PositiveSmallIntegerField(default=0)
#     order_price = models.DecimalField(max_digits=5, decimal_places=2)
#
#
# class Customer(ExtendedProfileMixin):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     store = models.ForeignKey('Store', on_delete=models.CASCADE)
#     address = models.ForeignKey(
#         'Address', on_delete=models.SET_NULL, blank=True, null=True
#     )
#
#     def __str__(self):
#         return f'{self.user.first_name} {self.user.last_name}'
#
#
# class Store(models.Model):
#     name = models.CharField(max_length=32, unique=True)
#     address = models.OneToOneField(
#         'Address', on_delete=models.SET_NULL, blank=True, null=True
#     )
#
#     def __str__(self):
#         return self.name
#
#
# class Staff(ExtendedProfileMixin):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     store = models.ForeignKey(Store, on_delete=models.CASCADE)
#     address = models.ForeignKey(
#         'Address', on_delete=models.SET_NULL, blank=True, null=True
#     )
#     avatar = models.ImageField(upload_to=upload_to_staff, blank=True,
#                                null=True)
#
#     def __str__(self):
#         return f'{self.user.first_name} {self.user.last_name}'
#
#
# class Payment(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=8, decimal_places=2, unique=True)
#     # payment_date = models.DateField()
#
#     def __str__(self):
#         return f"{self.customer.__str__} payment"
