from .common import GroupSerializer
from members.serializer.populated import PopulatedMemberSerializer
from jwt_auth.serializers.common import UserSerializer
from groupchat.serializers.populated import PopulatedGroupChatSerializer
from rest_framework import serializers
from ..models import Group
from games.serializers.common import GameSerializer


class PopulatedGroupSerializer(GroupSerializer):
    game = serializers.CharField(source='game.title')
    owner = UserSerializer()
    members = PopulatedMemberSerializer(many=True)
    groupchat_messages = PopulatedGroupChatSerializer(many=True)
    game_id = serializers.IntegerField(source='game.id', read_only=True)
    # 'like', 'dislike' or None for the logged-in user. Needs the request in the
    # serializer context (see GroupDetailView.get); None when it is missing.
    user_rating = serializers.SerializerMethodField()

    def get_user_rating(self, group):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        rating = group.ratings.filter(user=request.user).first()
        if not rating:
            return None
        return 'like' if rating.has_liked else 'dislike' if rating.has_disliked else None

    class Meta:
        model = Group
        fields = '__all__'
