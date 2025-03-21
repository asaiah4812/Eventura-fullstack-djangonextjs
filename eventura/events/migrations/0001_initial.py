# Generated by Django 5.1.7 on 2025-03-17 21:34

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('ticket_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_tickets', models.IntegerField()),
                ('available_tickets', models.IntegerField()),
                ('organizer_wallet', models.CharField(max_length=255)),
                ('image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('owner_wallet', models.CharField(max_length=255)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='events.event')),
            ],
            options={
                'ordering': ['-purchase_date'],
                'unique_together': {('event', 'owner_wallet')},
            },
        ),
    ]
