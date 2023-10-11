from rest_framework import serializers
from .models import Board, Comment, List, Card

from users.serializers import CustomUserSerializer

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'



class CardSerializer(serializers.ModelSerializer):

    # comments = CommentSerializer(many=True)
    
    class Meta:
        model = Card
        fields = '__all__'