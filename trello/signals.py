
from django.db.models.signals import pre_save
from django.dispatch import receiver

from trello.models import Board



@receiver(pre_save, sender=Board)
def update_bajarilmagan(sender, instance, **kwargs):
    if instance.is_time_expired():
        instance.bajarilmagan = True
        instance.status_active = False

        pre_save.disconnect(update_bajarilmagan, sender=Board)

        instance.save()

        pre_save.connect(update_bajarilmagan, sender=Board)
        