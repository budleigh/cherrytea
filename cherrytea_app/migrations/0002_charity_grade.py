# Generated by Django 2.0.1 on 2018-02-11 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cherrytea_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='charity',
            name='grade',
            field=models.PositiveIntegerField(default=75),
        ),
    ]
