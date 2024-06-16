# Generated by Django 5.0.4 on 2024-05-07 11:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Types',
            new_name='Element',
        ),
        migrations.CreateModel(
            name='CardListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.FloatField()),
                ('imageUrl', models.CharField(max_length=1000)),
                ('isActive', models.BooleanField(default=True)),
                ('listingType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='element', to='auctions.element')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CardListings',
        ),
    ]
