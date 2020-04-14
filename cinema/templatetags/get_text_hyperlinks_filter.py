"""
The custom filter for getting hyperlinks in a text.
"""

from re import search, sub
from django import template
from ..views import all_persons, all_films

register = template.Library()

info_by_persons_qs = all_persons.values_list(
    "pk", "user__first_name",  "user__last_name", named=True
)
info_by_films_qs = all_films.values_list(
    "pk", "title", named=True
)


@register.filter(name='get_text_hyperlinks')
def get_text_hyperlinks(text):
    for person in info_by_persons_qs:
        person_name = f'{person.user__first_name} {person.user__last_name}'
        match = search(f'\s?(?i:{person_name})\s?', text)
        if match:
            url_path = f'/cinema/movie-person/{person.pk}/'
            found_person = match.group()
            text = sub(
                found_person.strip(),
                f"<a href='{url_path}'>{person_name}</a>",
                text
            )
    for film in info_by_films_qs:
        match = search(f'\s?{film.title}\s?', text)
        if match:
            url_path = f'/cinema/film/{film.pk}/'
            found_film = match.group()
            text = sub(
                found_film.strip(),
                f"<a href='{url_path}'>{film.title}</a>",
                text
            )
    return text
