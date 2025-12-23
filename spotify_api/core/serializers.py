from rest_framework import serializers
from .models import User, MusicAction, SearchHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MusicActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicAction
        fields = '__all__'

class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = "__all__"
