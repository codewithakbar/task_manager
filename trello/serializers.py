from rest_framework import serializers
from .models import Board, TugatilmaganBoard, BajarilmaganBoard, Comment, List, Card

from users.serializers import CustomUserSerializer


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
        depth = 1



class TugatilmaganBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TugatilmaganBoard
        fields = '__all__'
        depth = 1



class BajarilmaganBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BajarilmaganBoard
        fields = '__all__'
        depth = 1



class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer(many=True)

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