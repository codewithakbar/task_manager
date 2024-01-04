from django.db.models.signals import post_save
from django.dispatch import receiver

from trello.models import Board

@receiver(post_save, sender=Board)
def move_board_to_bajarilmagan_board(sender, instance, **kwargs):
    instance.move_to_bajarilmagan_board()