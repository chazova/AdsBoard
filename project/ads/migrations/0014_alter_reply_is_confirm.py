# Generated by Django 4.2.6 on 2023-10-21 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0013_alter_reply_ad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='is_confirm',
            field=models.CharField(choices=[('true', 'Принят'), ('false', 'Не принят')], max_length=15, verbose_name='Статус'),
        ),
    ]
