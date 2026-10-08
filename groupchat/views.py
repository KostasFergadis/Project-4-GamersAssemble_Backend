from .models import GroupChat
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from groups.models import Group
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .serializers.common import GroupChatSerializer
from django.shortcuts import get_object_or_404
# Create your views here.


class GroupChatList(APIView):
    permission_classes = (IsAuthenticated,)

    def get_group(self, pk, name=None):
        try:
            if name:
                return Group.objects.get(name=name, pk=pk)
            else:
                return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise NotFound(detail="Can not find a group with that primary key")

    def get(self, request, pk):
        group = self.get_group(pk=pk)
        messages = GroupChat.objects.filter(
            group=group).order_by('-created_at')
        serialized_messages = GroupChatSerializer(messages, many=True)
        return Response(serialized_messages.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        group = self.get_group(pk=pk)
        message_text = (request.data.get('message_text') or '').strip()
        created_by_user = request.user

        if not message_text:
            raise ValidationError({'message_text': 'A message cannot be empty.'})
        if len(message_text) > 200:
            raise ValidationError(
                {'message_text': 'A message can be at most 200 characters long.'})

        if not group.members.filter(user=request.user).exists() and group.owner != request.user:
            raise PermissionDenied("You are not a member of this group.")

        message = GroupChat.objects.create(
            group=group, message_text=message_text, created_by=created_by_user)

        serialized_message = GroupChatSerializer(message)
        return Response(serialized_message.data, status=status.HTTP_201_CREATED)
