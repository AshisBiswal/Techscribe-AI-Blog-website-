# Generated by Django 4.0 on 2023-09-11 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_alter_blogmodel_title_addcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addcomment',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app1.blogmodel'),
        ),
    ]
