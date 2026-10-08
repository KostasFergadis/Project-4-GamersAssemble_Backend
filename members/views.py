from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Member
from groups.models import Group
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated


class RequestMembership(APIView):
    permission_classes = (IsAuthenticated,)

    def get_group(self, pk, name=None):
        try:
            if name:
                return Group.objects.get(name=name, pk=pk)
            else:
                return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise NotFound(
                detail="Can not find a group with that primary key")

    def post(self, request, pk):
        try:
            group_to_join = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            return Response({'error': 'Group does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        member, created = Member.objects.get_or_create(
            user=request.user, group=group_to_join)

        if created:
            # Add member to group members list
            group_to_join.members.add(member)
            group_to_join.save()

            return Response({'message': 'Member added successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Member already exists.'}, status=status.HTTP_400_BAD_REQUEST)


class RemoveMember(APIView):
    permission_classes = (IsAuthenticated,)

    def get_member(self, group_pk, member_pk):
        try:
            return Member.objects.get(pk=member_pk, group__pk=group_pk)
        except Member.DoesNotExist:
            raise NotFound(
                detail="Can not find a member with that primary key")

    def delete(self, request, group_pk, member_pk=None):
        if member_pk:
            member_to_remove = self.get_member(
                group_pk=group_pk, member_pk=member_pk)

            # Check if the user making the request is the owner of the group
            if request.user != member_to_remove.group.owner:
                return Response({'error': 'You do not have permission to remove this member.'}, status=status.HTTP_403_FORBIDDEN)

            member_to_remove.delete()
            return Response({'detail': 'Member succesfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            try:
                member_to_remove = Member.objects.get(
                    group__pk=group_pk, user=request.user)
            except Member.DoesNotExist:
                raise NotFound(detail="You are not a member of this group.")

            member_to_remove.delete()
            return Response({'detail': 'You have left the group.'}, status=status.HTTP_204_NO_CONTENT)
