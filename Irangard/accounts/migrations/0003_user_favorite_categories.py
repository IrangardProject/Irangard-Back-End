# Generated by Django 3.2.8 on 2023-04-29 12:03

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_get_notified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_categories',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('0', 'هنری'), ('1', 'علمی'), ('2', 'فرهنگی'), ('3', 'ورزشی'), ('4', 'سیاسی'), ('5', 'اجتماعی'), ('6', 'مذهبی'), ('7', 'تجاری'), ('8', 'سایر')], max_length=17, null=True),
        ),
    ]
