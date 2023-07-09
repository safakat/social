from rest_framework.serializers import ModelSerializer

from core.models.users_model import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"