# Generated by Django 3.2.8 on 2023-05-10 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0003_alter_tour_tour_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='city',
            field=models.CharField(default='Tehran', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tour',
            name='province',
            field=models.CharField(default='Tehran', max_length=255),
            preserve_default=False,
        ),
    ]
