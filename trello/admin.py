from django.contrib import admin
from .models import Board, Comment, List, Card, Member, BoardMember, Comment



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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'created_at',)
    list_filter = ('card', 'user',)
    search_fields = ('text', 'user__username',)



@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('boards',)
    search_fields = ('name',)



@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('board', 'member',)
    list_filter = ('board', 'member',)
    search_fields = ('board__name', 'member__name',)


