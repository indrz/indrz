from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from buildings.models import Organization, Campus


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    phone = models.CharField(verbose_name=_("Phone"), max_length=32,
                             blank=True, null=True, db_column='telephone')

    company = models.ForeignKey(Organization, null=True, blank=True)
    campus = models.ForeignKey(Campus, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
