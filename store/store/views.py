import json

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models.functions import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, FormView, ListView, UpdateView

import requests

from store.forms import ContactForm, OrderItemsForm, RegisterForm

from .models import Book, Genre, Order, OrderItem
from .tasks import contact_us_send_mail

User = get_user_model()


class RegisterFormView(SuccessMessageMixin, FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')
    success_message = 'Profile created'

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy('index')
    success_message = 'Profile updated'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


@method_decorator(cache_page(5), name='dispatch')
class BookListView(ListView):
    queryset = Book.objects.all().order_by('title')
    template_name = 'index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        p = Paginator(Book.objects.all().order_by('title'), self.paginate_by)
        context['articles'] = p.page(context['page_obj'].number)
        context['genre_list'] = Genre.objects.all()

        return context


@cache_page(5)
def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    books = genre.book_set.all().order_by('title')
    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    genre_list = Genre.objects.exclude(name=genre.name)

    context = {
        'genre': genre,
        'page_obj': page_obj,
        'genre_list': genre_list
    }

    return render(request, 'store/genre_detail_page.html', context)


@method_decorator(cache_page(5), name='dispatch')
class BookDetailView(SuccessMessageMixin, DetailView):
    model = Book
    template_name = 'store/book_details.html'


def contact_form(request):
    data = dict()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            data['form_is_valid'] = True
            contact_us_send_mail.delay(subject, message, from_email, ['admin@example.com'])
            messages.add_message(request, messages.SUCCESS, 'Message sent')
        else:
            data['form_is_valid'] = False
    else:
        form = ContactForm()
    context = {'form': form}
    data['html_form'] = render_to_string(template_name='includes/contact.html', context=context, request=request)
    return JsonResponse(data)


@login_required
def add_to_order(request, pk):
    book = get_object_or_404(Book, pk=pk)
    current_user = request.user
    order, created = Order.objects.get_or_create(status=2, user=current_user,
                                                 defaults={'user': current_user, 'comment': 'added automatically'})
    if OrderItem.objects.filter(book=book, order=order).exists():
        book_order_item = OrderItem.objects.get(book=book, order=order)
        book_order_item.quantity += 1
        book_order_item.save()
        messages.success(request, "Item already in cart! We added increased books quantity to +1")
        return redirect('index')
        # return reverse_lazy('index')
    else:
        OrderItem.objects.create(order=order, book=book)
        messages.success(request, "Item added to the cart!")
        return redirect('index')
        # return reverse_lazy('index')


@login_required
def order_items_list(request):
    current_user = request.user
    order, created = Order.objects.get_or_create(status=2, user=current_user,
                                                 defaults={'user': current_user,
                                                           'comment': 'added automatically'})
    order_items = OrderItem.objects.filter(order__id=order.id)
    return render(request, 'store/order_items_list.html', {'order': order, 'order_items': order_items})


def save_order_item_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            order = Order.objects.get(status=2, user=request.user)
            order_items = OrderItem.objects.filter(order__id=order.id)
            data['html_order_items_list'] = render_to_string('includes/partial_order_items_list.html', {
                'order_items': order_items
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context=context, request=request)
    return JsonResponse(data)


def order_item_update(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    if request.method == 'POST':
        form = OrderItemsForm(request.POST, instance=order_item)
    else:
        form = OrderItemsForm(instance=order_item)
    return save_order_item_form(request, form, 'includes/partial_order_item_update.html')


def order_items_delete(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    data = dict()
    if request.method == 'POST':
        order_item.delete()
        data['form_is_valid'] = True
        order = Order.objects.get(status=2, user=request.user)
        order_items = OrderItem.objects.filter(order__id=order.id)
        data['html_order_items_list'] = render_to_string('includes/partial_order_items_list.html', {
            'order_items': order_items
        })
    else:
        context = {'order_item': order_item}
        data['html_form'] = render_to_string('includes/partial_order_item_delete.html', context, request=request)
    return JsonResponse(data)


def order_send(request):
    url = 'http://warehouse:8002/orders/'
    order = Order.objects.get(status=2, user=request.user)
    order_items = OrderItem.objects.filter(order__id=order.id)

    order_items_list = []
    for record in order_items:
        order_item = {
            'id': record.id,
            'book': str(record.book.id),
            'quantity': record.quantity
        }
        order_items_list.append(order_item)
    data = json.dumps(
        {"id": str(order.id), "customer_mail": order.user.email,
         "order_date": str(datetime.datetime.now().date()),
         "order_items": order_items_list}
    )
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, headers=headers, data=data)
    if response.status_code == 201:
        order.status = 3
        order.save(update_fields=['status'])
        messages.success(request, "Item added to the cart!")
        return redirect('index')
    else:
        return redirect('update_profile')
