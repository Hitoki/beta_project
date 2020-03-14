from datetime import date, timedelta

from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Gender(models.Model):
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )
    value = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.value


class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=32, blank=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField()
    gender = models.ForeignKey(
        Gender, on_delete=models.SET_NULL, blank=True, null=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=True, null=True
    )

    @property
    def age(self):
        if self.birthday:
            return (date.today() - self.birthday) // timedelta(days=365.2425)
        return None

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.fullname


class OscarAwards(models.Model):
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.value)


class Actor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    oscar_awards = models.ForeignKey(
        OscarAwards, on_delete=models.SET_NULL, blank=True, null=True
    )


class Genre(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class BoxOffice(models.Model):
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    USA_gross = models.DecimalField(max_digits=11, decimal_places=2)
    world_gross = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return f'${self.budget}'


class ImdbRating(models.Model):
    value = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return str(self.value)


class MpaaRating(models.Model):
    value = models.CharField(max_length=10, default="Not Rated")

    def __str__(self):
        return self.value


class Film(models.Model):
    title = models.CharField(max_length=64)
    release_data = models.DateField(null=True, blank=True)
    run_time = models.TimeField()
    actor = models.ManyToManyField(Actor)
    genre = models.ManyToManyField(Genre)
    country = models.ManyToManyField(Country)
    box_office = models.OneToOneField(
        BoxOffice, on_delete=models.SET_NULL, blank=True, null=True
    )
    imdb_rating = models.ForeignKey(
        ImdbRating, on_delete=models.SET_NULL, blank=True, null=True
    )
    mpaa_rating = models.ForeignKey(
        MpaaRating, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.title


class NewsSource(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class NewsAuthor(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    created_at = models.DateTimeField()
    film = models.ManyToManyField(Film)
    actor = models.ManyToManyField(Actor)
    news_source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    news_author = models.ForeignKey(NewsAuthor, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# class Comment(models.Model):
#     comment_author = models.CharField(max_length=32)
#     text = models.CharField(max_length=512)
#     news = models.ForeignKey(News, on_delete=models.CASCADE)
#     film = models.ForeignKey(Film, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#
    # def __str__(self):
    #     return self.comment_author
