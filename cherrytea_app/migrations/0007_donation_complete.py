# Generated by Django 2.0.2 on 2018-02-11 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cherrytea_app', '0006_auto_20180211_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
