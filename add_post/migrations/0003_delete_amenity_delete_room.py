# Generated by Django 5.0.4 on 2024-04-24 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('add_post', '0002_alter_provides_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Amenity',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
