from rest_framework import generics
from core.serializers.auth_serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from core.models.users_model import User
from core.helpers import api_response

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            # send_onboard_eamil(request, user.email)
            user_data = {
                "access_token": str(token.access_token),
                "refresh_token": str(token),
            }
            return api_response(201, "An activation link has been send to your email. Please verify.", serializer.data, status=True)
        else:
            errors_list = [serializer.errors[error][0] for error in serializer.errors]
            return api_response(400, errors_list[0], {}, status=False)