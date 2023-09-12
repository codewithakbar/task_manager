from django.contrib import admin
from .models import Board, List, Card



@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title',)



@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'board',)
    list_filter = ('board',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'list',)
    list_filter = ('list__board', 'list',)
