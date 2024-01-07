
from django.db.models.signals import pre_save
from django.dispatch import receiver

from trello.models import Board



@receiver(pre_save, sender=Board)
def update_bajarilmagan(sender, instance, **kwargs):
    if instance.start_date and instance.end_date and instance.start_date > instance.end_date:
        instance.bajarilmagan = True
        instance.save()
        