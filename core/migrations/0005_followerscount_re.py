# Generated by Django 4.1 on 2022-11-02 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_followerscount'),
    ]

    operations = [
        migrations.AddField(
            model_name='followerscount',
            name='re',
            field=models.IntegerField(default=0),
        ),
    ]
