# Generated by Django 4.0 on 2023-09-20 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0018_alter_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogmodel',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
