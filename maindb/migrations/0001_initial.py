# Generated by Django 4.2.1 on 2023-05-16 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=500, verbose_name='Назва презентації')),
                ('author', models.TextField(max_length=250, verbose_name='Автор')),
                ('notes', models.CharField(max_length=250, verbose_name='Примітки')),
                ('time', models.DateTimeField(verbose_name='Час отримання')),
                ('link', models.TextField(verbose_name='Посилання на презентацію')),
                ('rating', models.TextField(default='', verbose_name='Оцінка')),
                ('group', models.CharField(max_length=250, verbose_name='Група')),
            ],
        ),
    ]
