# Generated by Django 4.0 on 2023-09-12 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_alter_addcomment_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addcomment',
            name='comment',
            field=models.TextField(default=None),
        ),
    ]
