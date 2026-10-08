from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializers.populated import PopulatedGameSerializer
from .serializers.common import GameSerializer
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, SAFE_METHODS

GAMES_PER_PAGE = 9


class IsAdminOrReadOnly(BasePermission):
    """Anyone can read games; only staff can create, edit or delete them."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or bool(
            request.user and request.user.is_staff)


class GameListView(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request):
        games = Game.objects.all().order_by('id')
        # ?search=zel filters by title (case-insensitive).
        search = request.GET.get('search', '').strip()
        if search:
            games = games.filter(title__icontains=search)

        # With ?page=N the response is paginated ({count, next, previous, results});
        # without it the full list is returned (used by the group creation form).
        if request.GET.get('page'):
            paginator = PageNumberPagination()
            paginator.page_size = GAMES_PER_PAGE
            result_page = paginator.paginate_queryset(games, request)
            serialized_products = GameSerializer(result_page, many=True)
            return paginator.get_paginated_response(serialized_products.data)
        else:
            serialized_products = GameSerializer(games, many=True)
            return Response(serialized_products.data, status=status.HTTP_200_OK)

    def post(self, request):
        game_to_add = GameSerializer(data=request.data)
        try:
            game_to_add.is_valid()
            game_to_add.save()
            return Response(game_to_add.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            res = {
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except:
            return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class GameDetailView(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get_game(self, _request, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise NotFound(
                detail="Can not find a game with that primary key")

    def get(self, request, pk):  # Add the request argument
        game = self.get_game(request, pk=pk)  # Pass the request argument
        serialized_game = PopulatedGameSerializer(game)
        return Response(serialized_game.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        game_to_edit = self.get_game(request, pk=pk)
        updated_game = GameSerializer(game_to_edit, data=request.data)
        try:
            updated_game.is_valid()
            updated_game.save()
            return Response(updated_game.data, status=status.HTTP_202_ACCEPTED)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            res = {"detail": "Unprocessable Entity"}
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        game_to_delete = self.get_game(request, pk=pk)
        game_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
