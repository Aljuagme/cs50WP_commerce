# Generated by Django 5.1.1 on 2024-09-13 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listing_options_bid_author_bid_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='author',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='created_at',
        ),
    ]