# Generated by Django 4.1.7 on 2023-04-17 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_class', models.CharField(max_length=10, verbose_name='Номер кабинета \n Пример : РИ120')),
                ('id_of_point', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Номер аудитории',
                'verbose_name_plural': 'Аудитории',
            },
        ),
        migrations.CreateModel(
            name='Institues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('ST', 'Улица'), ('RI', 'РИ'), ('T', 'Т')], max_length=2, verbose_name='Название')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Интститут',
                'verbose_name_plural': 'Интституты',
            },
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institue', models.CharField(choices=[('ST', 'Улица'), ('RI', 'РИ'), ('T', 'Т')], default='ST', max_length=2)),
                ('type', models.CharField(choices=[('0', 'улица'), ('1', 'коридор'), ('2', 'пре аудитория'), ('3', 'аудитория')], default='1', max_length=1)),
                ('relativeX', models.IntegerField()),
                ('relativeY', models.IntegerField()),
                ('connections', models.JSONField()),
                ('floor', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Тип точки | Этаж',
                'verbose_name_plural': 'Точки',
            },
        ),
    ]
