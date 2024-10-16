from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from common import utils
from .models import User
from . import serializers
from tweets.serializers import SimpleSerializer as TweetSerializer


class Users(APIView):

    def get(self, request):
        page = utils.get_page(request)

        # get users per page
        users = utils.get_page_items(page, User.objects.all())
        serializer = serializers.TinyUserSerializer(
            users,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):

        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required")

        serializer = serializers.PrivateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        # set password by calling set_password method for hashing it
        user.set_password(password)
        user.save()
        serializer = serializers.PrivateUserSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class Public(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User does not exist")

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class Tweets(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User does not exist")

    def get(self, request, pk):
        user = self.get_object(pk)
        page = utils.get_page(request)

        # get tweets per page from user
        tweets = utils.get_page_items(page, user.tweets.all())
        return Response(TweetSerializer(tweets, many=True).data)


class Password(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):

        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError("Old password and new password are required")

        if not user.check_password(old_password):
            raise ParseError("Old password is incorrect")

        user.set_password(new_password)
        user.save()
        return Response(status=204)


class PasswordManager(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User does not exist")

    def put(self, request, pk):

        login_user = request.user
        if not login_user.is_superuser and not login_user.is_staff:
            raise ParseError("You are not allowed to change password")

        user = self.get_object(pk)
        new_password = request.data.get("new_password")
        if not new_password:
            raise ParseError("New password are required")

        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if not user:
            return Response({"error": "wrong password"})

        login(request, user)
        return Response({"ok": "Welcome!"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.PrivateUserSerializer(request.user)
        return Response(serializer.data)
