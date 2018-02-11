# Generated by Django 2.0.2 on 2018-02-11 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cherrytea_app', '0005_auto_20180210_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timezone', models.CharField(default='America/New_York', max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='useroptions',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='options', to=settings.AUTH_USER_MODEL),
        ),
    ]