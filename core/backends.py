from core.helpers import api_response
from rest_framework import generics
from core.serializers.auth_serializers import MyTokenObtainPairSerializer

from core.models.users_model import User


class LoginAPIView(generics.GenericAPIView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request):
        try:
            user = User.objects.get(email = request.data['email'])
            credentials = {'username':user.username, 'password':request.data['password']}
            serializer = self.serializer_class(data=credentials)
        except:
            serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            return api_response(200, "Login success", serializer.data["tokens"], status=True)
        else:
            errors_list = [serializer.errors[error][0] for error in serializer.errors]
            return api_response(400, errors_list[0], {}, status=False)