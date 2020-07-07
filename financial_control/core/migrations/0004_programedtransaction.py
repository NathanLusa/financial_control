# Generated by Django 3.0.7 on 2020-07-07 14:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_transfer'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramedTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('initial_date', models.DateField(default=django.utils.timezone.now)),
                ('frequency', models.IntegerField(choices=[(0, 'Diary'), (1, 'Weekly'), (2, 'Monthly'), (3, 'Yearly')], default=0)),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('observation', models.CharField(blank=True, max_length=200, null=True)),
                ('last_verification', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='programed_transactions', to='core.Account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
