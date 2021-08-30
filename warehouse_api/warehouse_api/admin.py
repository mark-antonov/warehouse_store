from django.contrib import admin

from .models import Author, Book, BookInstance, Genre, Order, OrderItem


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['name']


class BooksInstanceInlineModelAdmin(admin.TabularInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_genre', 'display_authors', 'price', 'mark']
    search_fields = ['title']
    list_filter = ['mark', 'author', 'genre']
    filter_horizontal = ['author', 'genre']  # many-to-many relationship widget
    inlines = [BooksInstanceInlineModelAdmin]  # allows you to edit related objects on the same page as the parent obj.


@admin.register(BookInstance)
class BookInstanceModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'status', 'order_item']
    list_filter = ['status', 'order_item']


class OrderItemInlineModelAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0


def make_waiting(modeladmin, request, queryset):
    queryset.update(status=1)
make_waiting.short_description = 'Change order status to "Waiting"'  # noqa:E305


def make_in_progress(modeladmin, request, queryset):
    queryset.update(status=2)
make_in_progress.short_description = 'Change order status to "In progress"'  # noqa:E305


def make_done(modeladmin, request, queryset):
    queryset.update(status=3)
make_done.short_description = 'Change order status to "Done"'  # noqa:E305


def make_rejected(modeladmin, request, queryset):
    queryset.update(status=4)
make_rejected.short_description = 'Change order status to "Rejected"'  # noqa:E305


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['customer_mail', 'customer_name', 'order_date', 'shipped_date', 'status']
    date_hierarchy = 'order_date'  # date filter widget
    list_filter = ['status']
    inlines = [OrderItemInlineModelAdmin]
    actions = [make_waiting, make_in_progress, make_done, make_rejected]


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity']
    inlines = [BooksInstanceInlineModelAdmin]
