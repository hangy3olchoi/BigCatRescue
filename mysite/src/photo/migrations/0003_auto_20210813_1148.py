# Generated by Django 3.1.13 on 2021-08-13 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_auto_20210813_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.CharField(blank=True, max_length=100, verbose_name='One Line Description'),
        ),
    ]