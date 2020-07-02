# Generated by Django 3.0.7 on 2020-07-02 12:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200615_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_destinations', to='core.Account')),
                ('destination_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_transaction', to='core.Transaction')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_sources', to='core.Account')),
                ('source_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_transaction', to='core.Transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
