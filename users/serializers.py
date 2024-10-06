from rest_framework import serializers
from .models import User


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "tweets_count",
        ]
