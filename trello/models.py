from django.db import models




class Board(models.Model):
    title = models.CharField(max_length=100)


    def __str__(self):
        return self.title



class List(models.Model):
    title = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')

    def __str__(self):
        return self.title



class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return self.title

