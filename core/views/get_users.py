from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from core.models.users_model import User
from core.serializers.user_serializers import UserSerializer
from core.helpers import api_response

import sys

class UsersView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self,request):
        try:
            users = User.objects.all()
            print(users)
            print(users[0].password)
            serializer = UserSerializer(users,many = True)
            data = serializer.data
            return api_response(200, "All user details",data, status=True)
        except:
            print(sys.exc_info())
            return api_response(400, "Unable to get users", {}, status=False)