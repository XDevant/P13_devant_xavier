# Generated by Django 3.0 on 2022-10-15 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lettings', '0002_auto_20221016_0105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='letting_address', to='lettings.Address')),
            ],
        ),
    ]