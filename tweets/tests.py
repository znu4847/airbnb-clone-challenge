from rest_framework.test import APITestCase
from tweets.models import Tweet
from users.models import User


def create_user(username="testuser", password="testpassword"):
    return User.objects.create_user(
        username,
        password,
    )


def create_tweet(user, payload="Hello, world!"):
    return Tweet.objects.create(
        payload=payload,
        user=user,
    )


# Create your tests here.
class TweetsTestCase(APITestCase):

    URL = "/api/v1/tweets/"

    def setUp(self):
        user = create_user()
        self.user = user

    def test_get_no_data(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0, "test_get_no_data failed")

    def test_post_without_permission(self):
        response = self.client.post(self.URL, {"payload": "Hello, world!"})
        self.assertEqual(
            response.status_code, 403, "test_post_without_permission failed"
        )

    def test_post_with_permission(self):
        self.client.force_login(self.user)
        response = self.client.post(self.URL, {"payload": "Hello, world!"})
        self.assertEqual(response.status_code, 201, "test_post_with_permission failed")

    def test_get_with_data(self):
        response = self.client.get(self.URL)
        self.assertEqual(len(response.data), 0, "test_get_with_data#1 failed")
        create_tweet(self.user, "Hello, world!")
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1, "test_get_with_data#1 failed")


class DetailTestCase(APITestCase):

    URL = "/api/v1/tweets"

    def setUp(self):
        user = create_user()
        self.user = user
        tweet = create_tweet(user, "Hello, world!")
        self.tweet = tweet

    def test_get_fail(self):
        response = self.client.get(f"{self.URL}/777")
        self.assertEqual(response.status_code, 404, "test_get_fail failed")

    def test_get_success(self):
        response = self.client.get(f"{self.URL}/{self.tweet.pk}")
        self.assertEqual(response.status_code, 200, "test_get_success failed")

    def test_put_without_permission(self):
        response = self.client.put(
            f"{self.URL}/{self.tweet.pk}",
            {"payload": "Good morning!"},
        )
        self.assertEqual(
            response.status_code, 403, "test_put_without_permission failed"
        )

    def test_put_with_permission(self):
        self.client.force_login(self.user)
        response = self.client.put(
            f"{self.URL}/{self.tweet.pk}",
            {"payload": "Good morning!"},
        )
        self.assertEqual(response.status_code, 200, "test_put_with_permission#1 failed")
        self.assertEqual(
            response.data["payload"],
            "Good morning!",
            "test_put_with_permission#2 failed",
        )

    def test_put_with_wrong_user(self):
        another_user = create_user("another_user", "another_password")
        self.client.force_login(another_user)
        response = self.client.put(
            f"{self.URL}/{self.tweet.pk}",
            {"payload": "Good evening!"},
        )
        self.assertEqual(response.status_code, 403, "test_put_with_wrong_user failed")

    def test_delete_without_permission(self):
        response = self.client.delete(f"{self.URL}/{self.tweet.pk}")
        self.assertEqual(
            response.status_code, 403, "test_delete_without_permission failed"
        )

    def test_delete_with_permission(self):
        self.client.force_login(self.user)
        response = self.client.delete(f"{self.URL}/{self.tweet.pk}")
        self.assertEqual(
            response.status_code, 204, "test_delete_with_permission failed"
        )

    def test_delete_with_wrong_user(self):
        another_user = create_user("another_user", "another_password")
        self.client.force_login(another_user)
        response = self.client.delete(f"{self.URL}/{self.tweet.pk}")
        self.assertEqual(
            response.status_code, 403, "test_delete_with_wrong_user failed"
        )
