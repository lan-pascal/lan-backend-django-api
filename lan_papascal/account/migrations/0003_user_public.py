# Generated by Django 2.2.3 on 2019-07-25 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190723_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]