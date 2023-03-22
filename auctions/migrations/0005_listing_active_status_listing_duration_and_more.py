# Generated by Django 4.1.5 on 2023-03-21 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_listing_imageurl_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active_status',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='duration',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
