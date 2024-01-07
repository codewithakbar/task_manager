from django.db import models
from django.utils import timezone

from users.models import CustomUser
from datetime import datetime

from django.db.models.signals import pre_save
from django.dispatch import receiver

""" ################################   Boardlar   #################################### """

class Board(models.Model):
    title = models.CharField(max_length=100)
    user = models.ManyToManyField(CustomUser)
    status_active = models.BooleanField(default=True)

    bajarilmoqda = models.BooleanField(default=True)
    tekshiruvda = models.BooleanField(default=False)
    bajarilmagan = models.BooleanField(default=False)
    kutulmoqda = models.BooleanField(default=False)
    bajarilgan = models.BooleanField(default=False)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    # end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def formatted_end_date(self):
        if self.end_date:
            return self.end_date.strftime("%Y-%m-%dT%H:%M")
        return None

    def formatted_start_date(self):
        if self.start_date:
            return self.start_date.strftime("%Y-%m-%dT%H:%M")
        return None

    def is_time_expired(self):
        if self.end_date and self.start_date > self.end_date:
            self.bajarilmagan = True
            self.save()
            return True
        return False

    

class TugatilmaganBoard(models.Model):
    title = models.CharField(max_length=100)
    user = models.ManyToManyField(CustomUser)


    def __str__(self):
        return self.title


class BajarilmaganBoard(models.Model):
    title = models.CharField(max_length=100)
    user = models.ManyToManyField(CustomUser)


    def __str__(self):
        return self.title
    


class BajarilganBoard(models.Model):
    title = models.CharField(max_length=100)
    user = models.ManyToManyField(CustomUser)


    def __str__(self):
        return self.title


class ChekBoard(models.Model):
    title = models.CharField(max_length=100)
    user = models.ManyToManyField(CustomUser)


    def __str__(self):
        return self.title


#########################################################################################




class List(models.Model):
    title = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')

    def __str__(self):
        return self.title
    



################################################################################################



class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    due_date = models.DateField(null=True, blank=True)
    labels = models.ManyToManyField('Label', related_name='cards', blank=True)

    def __str__(self):
        return self.title




####################################################################################################


class Label(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=100)
    boards = models.ManyToManyField(Board, related_name='members', blank=True)

    def __str__(self):
        return self.name


class BoardMember(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.board} - {self.member}'


class Comment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(blank=True, null=True)
    user = models.ManyToManyField(CustomUser)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='comment_files/', blank=True, null=True)

    def __str__(self):
        return self.text



