# Generated by Django 4.2.6 on 2024-03-03 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('alpha2', models.TextField(max_length=2)),
                ('alpha3', models.TextField(max_length=3)),
                ('region', models.TextField()),
            ],
        ),
    ]
