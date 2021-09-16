import uuid

# import requests
# from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django_lifecycle import LifecycleModelMixin  # hook, AFTER_UPDATE


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4,
    #                       help_text="Unique ID for this particular book across whole library")
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author, verbose_name='book authors')
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    genre = models.ManyToManyField(Genre, verbose_name='genre')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mark = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def display_authors(self):
        """Creates a string for the Author. This is required to display author in Admin."""
        return ', '.join([author.name for author in self.author.all()[:3]])

    display_authors.short_description = 'Authors'

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genres'


class Order(LifecycleModelMixin, models.Model):
    class OrderStatus(models.IntegerChoices):
        WAITING = 1, 'Waiting'
        IN_PROGRESS = 2, 'In progress'
        DONE = 3, 'Done'
        REJECTED = 4, 'Rejected'

    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, help_text='Unique ID for this order across whole store'
    )
    customer_mail = models.EmailField(help_text='Customer e-mail address')
    customer_name = models.CharField(max_length=100)
    order_date = models.DateField(help_text='Date when order was created')
    shipped_date = models.DateField(null=True, blank=True, help_text='Date when order moved to Done status')
    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices, default=OrderStatus.WAITING, help_text='Order status'
    )
    comment = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.id}'

    # @hook(AFTER_UPDATE, when='status', changes_to=3)
    # def order_status_done_email(self):
    #     send_mail(
    #         subject="Your order was Done",
    #         message="Your order was Done",
    #         from_email="admin@admin.com", This will have no effect is you have set DEFAULT_FROM_EMAIL in settings.py
    #         recipient_list=[f'{self.customer_mail}', ],  # This is a list
    #         fail_silently=False  # Set this to False so that you will be noticed in any exception raised
    #     )
    #
    #     url = 'http://shop:8001/store/orders_api/'
    #     requests.post(url=url, json={'id': f'{self.id}', 'status': 4})
    #
    # @hook(AFTER_UPDATE, when='status', changes_to=4)
    # def order_status_rejected_email(self):
    #     from django.core.mail import send_mail
    #
    #     send_mail(
    #         subject="Your order was rejected",
    #         message="Your order was rejected",
    #         from_email="admin@admin.com",  This will have no effect is you have set DEFAULT_FROM_EMAIL in settings.py
    #         recipient_list=[f'{self.customer_mail}'],  # This is a list
    #         fail_silently=False  # Set this to False so that you will be noticed in any exception raised
    #     )
    #     url = 'http://shop:8001/store/orders_api/'
    #     requests.post(url=url, json={'id': f'{self.id}', 'status': 5})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(help_text='Books quantity', default=1)

    def __str__(self):
        return f'{self.id}'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    class SellStatus(models.IntegerChoices):
        IN_STOCK = 1, 'In stock'
        RESERVED = 2, 'Reserved'
        SOLD = 3, 'Sold'

    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole store'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='order_item')
    status = models.PositiveSmallIntegerField(
        choices=SellStatus.choices, default=SellStatus.IN_STOCK, blank=True, help_text='Book status'
    )

    def __str__(self):
        return f'{self.id} ({self.book.title})'
