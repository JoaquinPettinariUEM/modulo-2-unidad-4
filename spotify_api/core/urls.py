from django.urls import path
from .views import (
    UserList, UserDetail,
    SpotifySearch,
    SpotifySearchHistory,
    SpotifyAction,
    SpotifyActionHistory,
)

urlpatterns = [
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),

    path("spotify/search/", SpotifySearch.as_view()),
    path("spotify/search/<int:user_id>/", SpotifySearchHistory.as_view()),
    path("spotify/action/", SpotifyActionHistory.as_view()),
    path("spotify/action/<int:id>/", SpotifyAction.as_view()),

]
