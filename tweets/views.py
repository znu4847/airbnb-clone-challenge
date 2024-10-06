from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Tweet
from .serializers import TweetSerializer


# Create your views here.
@api_view(["GET"])
def see_all_tweets(request):
    print("-----hello it's tweets api")
    tweets = Tweet.objects.all()
    serializer = TweetSerializer(tweets, many=True)
    print("-----tweets", serializer.data)
    return Response(serializer.data)
