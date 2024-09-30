from django.db import models
from common.models import CommonModel


class Tweet(CommonModel):
    """Tweet Model Definition"""

    payload = models.TextField(max_length=180)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="tweets"
    )

    def __str__(self):
        return f"Tweet: {{ user: {self.user}, tweet: {self.payload}, created_at: {super().created_str()}}}"

    def like_count(self):
        return self.likes.count()

    like_count.short_description = "Number of Likes"


class Like(CommonModel):
    """Like Model Definition"""

    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="likes"
    )

    def __str__(self):
        return f"Like: {{ user: {self.user}, tweet: {self.tweet}, created_at: {super().created_str()}}}"
