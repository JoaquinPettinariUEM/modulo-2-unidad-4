from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, SearchHistory, MusicAction
from .serializers import (
    UserSerializer,
    MusicActionSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from core.models import User, SearchHistory, MusicAction
from core.services.spotify import get_spotify_search
from core.models import SearchTypeEnum, ActionEnum

# User endpoints
class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        return Response(UserSerializer(user).data)

    def put(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Spotify
class SpotifySearch(APIView):
    def get(self, request):
        query = request.query_params.get("query")
        user_id = request.query_params.get("user_id")
        _type = request.query_params.get("type", SearchTypeEnum.TRACK)

        if not query or not user_id:
            return Response(
                {"error": "query and user_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, id=user_id)

        spotify_response = get_spotify_search(query, _type)

        SearchHistory.objects.create(
            user=user,
            query=query,
            type=_type,
        )

        return Response(spotify_response)

class SpotifySearchHistory(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        searches = SearchHistory.objects.filter(user=user)

        data = [
            {
                "id": search.id, # type: ignore
                "query": search.query,
                "type": search.type,
            }
            for search in searches
        ]

        return Response(data)

class SpotifyAction(APIView):
    # TODO: should i create splitted endpoints or how can i make a difference between those two?
    # this should be user ID
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        actions = user.music_actions.all() # type: ignore

        serializer = MusicActionSerializer(actions, many=True)
        return Response(serializer.data)

    # this should be action ID
    def delete(self, request, id):
        action = get_object_or_404(MusicAction, id=id)
        action.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SpotifyActionHistory(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        spotify_id = request.data.get("spotify_id")
        action = request.data.get("action")
        search_type = request.data.get("type", SearchTypeEnum.TRACK)
        if action not in ActionEnum.values:
            return Response(
                {"error": "Invalid action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if search_type not in SearchTypeEnum.values:
            return Response(
                {"error": "Invalid type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, id=user_id)

        music_action = MusicAction.objects.create(
            user=user,
            spotify_id=spotify_id,
            action=action,
            type=type,
        )

        return Response(
            {
                "message": "Action saved",
                "id": music_action.id, # type: ignore
            },
            status=status.HTTP_201_CREATED,
        )
