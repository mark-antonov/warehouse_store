from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from store.models import OrderItem

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True)
    from_email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class OrderItemsForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('book', 'book', 'book', 'quantity')
