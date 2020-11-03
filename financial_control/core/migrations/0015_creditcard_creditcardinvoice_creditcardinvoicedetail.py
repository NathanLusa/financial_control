# Generated by Django 3.1.2 on 2020-11-03 13:13

import core.common.model_fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20201009_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=100)),
                ('payment_day', core.common.model_fields.IntegerRangeField()),
                ('payment_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_cards', to='core.account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CreditCardInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_date', models.DateField()),
                ('is_open', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=1)),
                ('credit_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='core.creditcard')),
                ('payment_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_card_invoices', to='core.account')),
                ('payment_transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='credit_card_invoice_payment', to='core.transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CreditCardInvoiceDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('date', models.DateField()),
                ('observation', models.CharField(blank=True, max_length=200, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.category')),
                ('credit_card_invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_details', to='core.creditcardinvoice')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
