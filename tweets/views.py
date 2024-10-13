from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from common import utils
from .models import Tweet
from . import serializers


class Tweets(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        page = utils.get_page(request)

        # get users per page
        tweets = utils.get_page_items(page, Tweet.objects.all())
        serializer = serializers.SimpleSerializer(
            tweets,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):

        serializer = serializers.UpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        tweet = serializer.save(user=request.user)
        serializer = serializers.UpdateSerializer(tweet)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class Detail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise NotFound("Tweet does not exist")

    def get(self, request, pk):
        tweet = self.get_object(pk)
        serializer = serializers.SimpleSerializer(tweet)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.user != request.user:
            raise PermissionDenied
        serializer = serializers.UpdateSerializer(
            tweet,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        tweet = serializer.save()
        serializer = serializers.SimpleSerializer(tweet)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.user != request.user:
            raise PermissionDenied
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
