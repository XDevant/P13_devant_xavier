# Generated by Django 3.0 on 2022-10-15 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oc_lettings_site', '0002_auto_20221016_0126'),
        ('lettings', '0002_auto_20221016_0105'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
    ]