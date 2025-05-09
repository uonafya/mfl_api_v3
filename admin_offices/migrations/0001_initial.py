# Generated by Django 4.2.7 on 2025-04-21 09:28

import common.fields
import common.models.base
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminOffice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text='Indicates whether the record has been retired?')),
                ('search', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('code', common.fields.SequenceField(blank=True, editable=False, help_text='A unique number to identify the admin office.', unique=True)),
                ('old_code', models.IntegerField(blank=True, null=True)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('is_national', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(common.models.base.SequenceMixin, models.Model),
        ),
    ]
