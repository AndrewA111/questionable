# Generated by Django 2.1.5 on 2020-03-17 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20200313_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='images/29511773_1650373861750562_982140361914727316_n.jpg', upload_to='images/'),
        ),
    ]
