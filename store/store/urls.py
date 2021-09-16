from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='index'),
    path('genre/<int:pk>', views.genre_detail, name='genre-detail'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('contact/', views.contact_form, name='contact'),
    path('add_to_order/<int:pk>', views.add_to_order, name='add_to_order'),
    path('order/', views.order_items_list, name='order'),
    path('order/send/', views.order_send, name='order_send'),
    path('order/<int:pk>/update/', views.order_item_update, name='order_update'),
    path('order/<int:pk>/delete/', views.order_items_delete, name='order_item_delete'),
]
