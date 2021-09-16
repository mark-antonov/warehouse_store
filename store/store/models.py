import uuid

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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


class Order(models.Model):
    class OrderStatus(models.IntegerChoices):
        WAITING = 1, 'Waiting'
        IN_PROGRESS = 2, 'In progress'
        SENT = 3, 'Sent'
        DONE = 4, 'Done'
        REJECTED = 5, 'Rejected'

    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, help_text='Unique ID for this order across whole store'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField(help_text='Date when order was created', null=True, blank=True)
    shipped_date = models.DateField(null=True, blank=True, help_text='Date when order moved to Done status')
    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices, default=OrderStatus.WAITING, help_text='Order status'
    )
    comment = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.id}'

    def order_id(self):
        return self.id.__str__()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(help_text='Books quantity', default=1)

    def __str__(self):
        return f'{self.id}, {self.book}'
