from datetime import datetime, timezone
from rest_framework import serializers

from users.models import Departaments
from users.serializers import CustomUserSerializer

from .models import BajarilganBoard, Board, ChekBoard, TugatilmaganBoard, BajarilmaganBoard, Comment, List, Card

class CustomDateTimeField(serializers.ReadOnlyField):
    def to_representation(self, value):
        if value is not None:
            return value.strftime('%Y-%m-%d')
        return None

    
    
class BoardSerializer(serializers.ModelSerializer):
    # end_date = CustomDateTimeField(read_only=True)


    class Meta:
        model = Board
        fields = '__all__'
        depth = 1


class DepartamentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departaments
        fields = '__all__'
        depth = 1



class TugatilmaganBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TugatilmaganBoard
        fields = '__all__'
        depth = 1


class ChekBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChekBoard
        fields = '__all__'
        depth = 1



class BajarilmaganBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BajarilmaganBoard
        fields = '__all__'
        depth = 1


class BajarilganSerializer(serializers.ModelSerializer):
    class Meta:
        model = BajarilganBoard
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