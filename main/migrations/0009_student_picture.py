# Generated by Django 2.1.5 on 2020-03-11 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200308_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='picture',
            field=models.ImageField(default='default.jpg', upload_to='static/images/'),
        ),
    ]
