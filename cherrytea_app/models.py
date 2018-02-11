from django.db import models
from django.contrib.auth.models import User

from cherrytea_app.util import day_map_reverse


class UserOptions(models.Model):
    user = models.OneToOneField(User, related_name='options', on_delete=models.CASCADE)
    timezone = models.CharField(max_length=255, default='America/New_York')


class CharityGroup(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    charities = models.ManyToManyField('Charity')
    image = models.ImageField()


class Charity(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    category = models.CharField(max_length=100, choices=(
        ('HEALTH', 'Health'),
        ('POVER', 'Poverty'),
        ('TRAFF', 'Trafficking/Slavery'),
        ('ANIM', 'Animals'),
    ))
    grade = models.PositiveIntegerField(default=75)


class Donation(models.Model):
    group = models.ForeignKey(CharityGroup, related_name='donations', on_delete=models.DO_NOTHING)
    amount = models.PositiveIntegerField()
    user = models.ForeignKey(User, related_name='donations', on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now_add=True, db_index=True)


class DonationPlan(models.Model):
    group = models.ForeignKey(CharityGroup, related_name='plans', on_delete=models.DO_NOTHING)
    amount = models.PositiveIntegerField()
    user = models.ForeignKey(User, related_name='plans', on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, db_index=True)
    day = models.PositiveIntegerField(default=6)  # weekday int
    last_fulfilled = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=(
        ('ACT', 'active'),
        ('SUS', 'suspended'),
    ))
    total_donated = models.PositiveIntegerField(default=0)

    @property
    def human_day(self):
        return day_map_reverse[self.day]
