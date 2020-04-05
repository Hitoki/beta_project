from django.contrib import admin

from .models import (Country, Genre, Language, Distributor, ImdbRating,
                     MpaaRating, Film, CinemaPerson, CinemaProfession,
                     CinemaFilmPersonProfession, Product, News)


class CountryAdmin(admin.ModelAdmin):
    pass


class GenreAdmin(admin.ModelAdmin):
    pass


class LanguageAdmin(admin.ModelAdmin):
    pass


class DistributorAdmin(admin.ModelAdmin):
    pass


class ImdbRatingAdmin(admin.ModelAdmin):
    pass


class MpaaRatingAdmin(admin.ModelAdmin):
    pass


class FilmAdmin(admin.ModelAdmin):
    pass


class CinemaPersonAdmin(admin.ModelAdmin):
    pass


class CinemaProfessionAdmin(admin.ModelAdmin):
    pass


class CinemaFilmPersonProfessionAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class NewsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Country, CountryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Distributor, DistributorAdmin)
admin.site.register(ImdbRating, ImdbRatingAdmin)
admin.site.register(MpaaRating, MpaaRatingAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(CinemaPerson, CinemaPersonAdmin)
admin.site.register(CinemaProfession, CinemaProfessionAdmin)
admin.site.register(CinemaFilmPersonProfession, CinemaFilmPersonProfessionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(News, NewsAdmin)
