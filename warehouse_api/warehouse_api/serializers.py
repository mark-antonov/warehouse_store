from rest_framework import serializers

from .models import Author, Book, BookInstance, Genre, Order, OrderItem


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['url', 'id', 'name']


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['url', 'id', 'name']


class BookInstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookInstance
        fields = ['url', 'id', 'book', 'order_item', 'status']


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['url', 'id', 'order', 'book', 'quantity']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    books = BookInstanceSerializer(source='bookinstance_set', many=True)
    author = GenreSerializer(read_only=True, many=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        many = True
        model = Book
        fields = ['url', 'id', 'title', 'author', 'summary', 'genre', 'price', 'mark', 'books']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    order_items = OrderItemSerializer(source='orderitem_set', many=True)

    class Meta:
        model = Order
        fields = ['url', 'id', 'customer_mail', 'customer_name', 'order_date', 'shipped_date', 'status', 'order_items']

    def create(self, validated_data):
        order_items_validated_data = validated_data.pop('orderitem_set')
        order = Order.objects.create(**validated_data)
        order_items_serializer = self.fields['order_items']
        for each in order_items_validated_data:
            each['order'] = order
        order_items_serializer.create(order_items_validated_data)
        return order, order_items_validated_data
