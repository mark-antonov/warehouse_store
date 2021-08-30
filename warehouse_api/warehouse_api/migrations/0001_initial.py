# Generated by Django 3.2.6 on 2021-08-24 20:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(help_text='Enter a brief description of the book', max_length=1000)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('mark', models.FloatField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('author', models.ManyToManyField(to='warehouse_api.Author', verbose_name='book authors')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this order across whole library', primary_key=True, serialize=False)),
                ('customer_mail', models.EmailField(help_text='Customer e-mail address', max_length=254)),
                ('customer_name', models.CharField(max_length=100)),
                ('order_date', models.DateField(help_text='Date when order was created')),
                ('shipped_date', models.DateField(blank=True, help_text='Date when order moved to Done status', null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Waiting'), (2, 'In progress'), (3, 'Done'), (4, 'Rejected')], default=1, help_text='Order status')),
                ('comment', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, help_text='Books quantity')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse_api.book')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse_api.order')),
            ],
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'In stock'), (2, 'Reserved'), (3, 'Sold')], default=1, help_text='Book status')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse_api.book')),
                ('order_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='warehouse_api.orderitem')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(to='warehouse_api.Genre', verbose_name='genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse_api.publisher', verbose_name='book publisher'),
        ),
    ]