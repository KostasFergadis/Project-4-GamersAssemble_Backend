from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from groups.models import Group
from members.models import Member
from .models import Rating


class RateGroup(APIView):
    """
    Shared logic for liking and disliking a group.

    Only members can rate a group. Each member has one vote per group:
    - voting the same way again removes the vote (a toggle),
    - voting the other way switches the vote.
    The group's counters are kept in sync with the Rating rows.
    """
    permission_classes = (IsAuthenticated,)
    liking = True  # overridden in Dislike

    def post(self, request, pk):
        with transaction.atomic():
            try:
                group = Group.objects.select_for_update().get(pk=pk)
            except Group.DoesNotExist:
                raise NotFound(detail='Can not find a group with that primary key')

            if not Member.objects.filter(group=group, user=request.user).exists():
                raise PermissionDenied(detail='Join the group to rate it.')

            rating, _ = Rating.objects.get_or_create(group=group, user=request.user)

            if self.liking:
                if rating.has_liked:
                    rating.has_liked = False
                    group.likes = max(group.likes - 1, 0)
                else:
                    if rating.has_disliked:
                        rating.has_disliked = False
                        group.dislikes = max(group.dislikes - 1, 0)
                    rating.has_liked = True
                    group.likes += 1
            else:
                if rating.has_disliked:
                    rating.has_disliked = False
                    group.dislikes = max(group.dislikes - 1, 0)
                else:
                    if rating.has_liked:
                        rating.has_liked = False
                        group.likes = max(group.likes - 1, 0)
                    rating.has_disliked = True
                    group.dislikes += 1

            rating.likes = int(rating.has_liked)
            rating.dislikes = int(rating.has_disliked)
            rating.save()
            group.save()

        user_rating = 'like' if rating.has_liked else 'dislike' if rating.has_disliked else None
        return Response(
            {'likes': group.likes, 'dislikes': group.dislikes, 'user_rating': user_rating},
            status=status.HTTP_200_OK,
        )


class Like(RateGroup):
    liking = True


class Dislike(RateGroup):
    liking = False
