# Generated by Django 4.0.4 on 2022-05-25 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_alter_article_id_alter_customuser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='Заголовок'),
        ),
    ]
