from rest_framework import viewsets

from .models import Author, Book, BookInstance, Genre, Order, OrderItem
from .serializers import AuthorSerializer, BookInstanceSerializer, BookSerializer, GenreSerializer, OrderItemSerializer
from .serializers import OrderSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer


class BookInstanceViewSet(viewsets.ModelViewSet):
    queryset = BookInstance.objects.all().order_by('book__title')
    serializer_class = BookInstanceSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by('order')
    serializer_class = OrderItemSerializer
