from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from groups.models import Group
from .models import Rating


class RateGroup(APIView):
    """
    Shared logic for liking and disliking a group.

    Each user has at most one Rating row per group and can hold one opinion at a
    time: rating the other way switches the vote, and repeating the same vote
    changes nothing. The group's counters are kept in sync with those rows.
    """
    permission_classes = (IsAuthenticated,)
    liking = True  # overridden in Dislike

    def post(self, request, pk):
        with transaction.atomic():
            try:
                group = Group.objects.select_for_update().get(pk=pk)
            except Group.DoesNotExist:
                raise NotFound(detail='Can not find a group with that primary key')

            rating, _ = Rating.objects.get_or_create(group=group, user=request.user)

            if self.liking and not rating.has_liked:
                if rating.has_disliked:
                    rating.has_disliked = False
                    group.dislikes = max(group.dislikes - 1, 0)
                rating.has_liked = True
                group.likes += 1
            elif not self.liking and not rating.has_disliked:
                if rating.has_liked:
                    rating.has_liked = False
                    group.likes = max(group.likes - 1, 0)
                rating.has_disliked = True
                group.dislikes += 1

            rating.likes = int(rating.has_liked)
            rating.dislikes = int(rating.has_disliked)
            rating.save()
            group.save()

        return Response(
            {'likes': group.likes, 'dislikes': group.dislikes},
            status=status.HTTP_200_OK,
        )


class Like(RateGroup):
    liking = True


class Dislike(RateGroup):
    liking = False
