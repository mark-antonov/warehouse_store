from django.contrib import admin

from .models import Author, Book, Genre, Order, OrderItem


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_genre', 'display_authors', 'price', 'mark']
    search_fields = ['title']
    list_filter = ['mark', 'author', 'genre']
    filter_horizontal = ['author', 'genre']  # many-to-many relationship widget


class OrderItemInlineModelAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0


def make_waiting(modeladmin, request, queryset):
    queryset.update(status=1)


make_waiting.short_description = 'Change order status to "Waiting"'  # noqa:E305


def make_in_progress(modeladmin, request, queryset):
    queryset.update(status=2)


make_in_progress.short_description = 'Change order status to "In progress"'  # noqa:E305


def make_sent(modeladmin, request, queryset):
    queryset.update(status=3)


make_sent.short_description = 'Change order status to "Sent"'  # noqa:E305


def make_done(modeladmin, request, queryset):
    queryset.update(status=4)


make_done.short_description = 'Change order status to "Done"'  # noqa:E305


def make_rejected(modeladmin, request, queryset):
    queryset.update(status=5)


make_rejected.short_description = 'Change order status to "Rejected"'  # noqa:E305


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'shipped_date', 'status']
    date_hierarchy = 'order_date'  # date filter widget
    list_filter = ['status']
    inlines = [OrderItemInlineModelAdmin]
    actions = [make_waiting, make_in_progress, make_sent, make_done, make_rejected]


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity']
