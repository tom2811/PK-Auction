# Generated by Django 5.0.4 on 2024-05-07 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_rename_types_element_cardlisting_delete_cardlistings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='element',
            old_name='type',
            new_name='elementType',
        ),
    ]
