
# Mission:
Django Rest Framework을 사용하여, 아래와 같은 기능을 갖고있는 REST API 를 빌드하세요.

# API Routes
ModelSerializer 그리고 APIView 를 사용하여 아래 routes 를 구현하세요.

## Tweets
- GET /api/v1/tweets: See all tweets [x]
- POST /api/v1/tweets: Create a tweet [x]
- GET /api/v1/tweets/<int:pk>: See a tweet [x]
- PUT /api/v1/tweets/<int:pk>: Edit a tweet [x]
- DELETE /api/v1/tweets/<int:pk>: Delete a tweet [x]

## Users
- GET /api/v1/users: See all users [x]
- POST /api/v1/users: Create a user account with password [x]
- GET /api/v1/users/<int:pk>: See user profile [x]
- GET /api/v1/users/<int:pk>/tweets: See tweets by a user [x]
- PUT /api/v1/users/password: Change password of logged in user. [x]
- POST /api/v1/users/login: Log user in [x]
- POST /api/v1/users/logout: Log user out [x]

# Authentication
- UsernameAuthentication라는 이름의 authentication class를 빌드하세요.
- UsernameAuthentication 는 반드시 BaseAuthentication에서 extend 되어야 합니다.
- X-USERNAME 헤더를 사용하는 유저를 찾으세요.

# Testing
다음과 같은 URL 과 메소드를 위한 APITestCase 를 작성하세요.

- /api/v1/tweets: Test GET and POST methods
- /api/v1/tweets/<int:pk>: Test GET, PUT and DELETE methods