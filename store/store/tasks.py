from celery import shared_task

from django.core.mail import send_mail as django_send_mail

import requests

from store.models import Book, Genre


@shared_task
def contact_us_send_mail(subject, message, from_email, recipient_list):
    django_send_mail(subject, message, from_email, recipient_list)


@shared_task
def book_sync():
    url = 'http://warehouse:8001/books'
    response = requests.get(url=url).json()

    for counter, book in enumerate(response):
        if Book.objects.filter(id=book['id']).exists():
            continue
        else:
            genre_list = []

            for genre_resp in book['genre']:
                genre, created = Genre.objects.get_or_create(name=genre_resp['name'])
                genre_list.append(genre.id)

            book = Book(
                id=book['id'],
                title=book['title'],
                author=book['author'],
                summary=book['summary'],
                genre=book['genre'],
                price=book['price'],
                mark=book['mark'],
            )
            book.save()
            for genre in genre_list:
                book.genre.add(genre)
                book.save()

    print('Sync is done')  # noqa:T001
