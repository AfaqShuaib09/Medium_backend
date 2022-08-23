# Generated by Django 4.1 on 2022-08-23 17:26

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0002_alter_profile_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='PK', help_text='your country', max_length=2),
        ),
    ]
