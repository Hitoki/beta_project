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

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ["user__first_name", "user__last_name"]


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

    class Meta:
        ordering = ["title"]


class CinemaProfession(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["pk"]


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
        ordering = ["-film__oscar_awards", ]
