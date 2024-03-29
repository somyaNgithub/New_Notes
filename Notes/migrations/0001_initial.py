# Generated by Django 4.2.5 on 2024-01-04 14:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('N_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('U_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.customuser')),
            ],
        ),
    ]
