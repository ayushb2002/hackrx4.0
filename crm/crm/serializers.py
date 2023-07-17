from rest_framework import serializers
from accounts.models import InstagramProfile
class InstagramProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramProfile
        fields = ['username', 'verified', 'followers', 'following', 'biography', 'post_urls']
