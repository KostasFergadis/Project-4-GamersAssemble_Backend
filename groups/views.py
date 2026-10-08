from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import Game
from .models import Group
from .serializers.common import GroupSerializer
from .serializers.populated import PopulatedGroupSerializer


def flatten_errors(errors):
    """Turn DRF's {field: [messages]} into one readable string for the frontend."""
    return ' '.join(
        f'{field}: {message}' for field, messages in errors.items() for message in messages)


class GroupListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, _request):
        groups = Group.objects.all()
        serialized_groups = GroupSerializer(groups, many=True)
        return Response(serialized_groups.data, status=status.HTTP_200_OK)

    def post(self, request):
        # The frontend identifies the game by its title.
        try:
            game = Game.objects.get(title=request.data.get('title'))
        except Game.DoesNotExist:
            return Response({'error': 'Please select a game for the group.'},
                            status=status.HTTP_400_BAD_REQUEST)

        group_to_add = GroupSerializer(data={
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'game': game.id,
            'owner': request.user.id,
        })
        if not group_to_add.is_valid():
            return Response({'error': flatten_errors(group_to_add.errors)},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        group_to_add.save()
        return Response(group_to_add.data, status=status.HTTP_201_CREATED)


class GroupDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_group(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise NotFound(detail='Can not find a group with that primary key')

    def get(self, request, pk):
        group = self.get_group(pk)
        serialized_group = PopulatedGroupSerializer(group, context={'request': request})
        return Response(serialized_group.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        group_to_edit = self.get_group(pk)
        if request.user != group_to_edit.owner:
            return Response({'error': 'Only the owner of the group can update it.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Only the name and description can be edited; ownership, game, members and
        # the like counters are managed elsewhere.
        data = {key: request.data[key]
                for key in ('name', 'description') if key in request.data}
        updated_group = GroupSerializer(group_to_edit, data=data, partial=True)
        if not updated_group.is_valid():
            return Response({'error': flatten_errors(updated_group.errors)},
                            status=status.HTTP_400_BAD_REQUEST)

        updated_group.save()
        return Response(updated_group.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        group_to_delete = self.get_group(pk)
        if request.user != group_to_delete.owner:
            return Response({'error': 'Only the owner of the group can delete it.'},
                            status=status.HTTP_403_FORBIDDEN)

        group_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
