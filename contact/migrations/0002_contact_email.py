# Generated by Django 4.0.6 on 2022-07-18 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='email',
            field=models.EmailField(default='Default Email', max_length=255),
        ),
    ]
