from rest_framework import serializers

from core.models.users_model import User

from core.helpers import password_validation

from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainPairSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj["username"])
        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)
        data = {"refresh": refresh, "access": access}
        # data["first_name"] = user.first_name
        # if user.role == None:
        #     data["role"] = " "
        # else:
        #     data["role"] = user.role

        return data

    class Meta:
        model = User
        fields = ["username", "password", "tokens"]

class RegisterSerializer(serializers.ModelSerializer):
    retype_password = serializers.CharField(required=True, style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "date_of_birth",
            "password",
            "retype_password",
        )
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }

    def validate(self, attrs):
        usernmae = attrs.get("usernmae")
        email = attrs.get("email")
        password = attrs.get("password")
        retype_password = attrs.get("retype_password")
        if User.objects.filter(username=usernmae):
            raise serializers.ValidationError("username already exists")
        if User.objects.filter(email=email):
            raise serializers.ValidationError("email already exists")
        if password != retype_password:
            raise serializers.ValidationError("passwords must match")
        pwd_err = password_validation(password)
        if pwd_err:
            raise serializers.ValidationError(pwd_err)

        return super().validate(attrs)
    
    def create(self, attrs):
        usernmae = attrs["username"]
        email = attrs["email"]
        date_of_birth = attrs["date_of_birth"]
        password = attrs["password"]

        user = User(
            email=email,
            username=usernmae,
            date_of_birth = date_of_birth
        )
        user.set_password(password)
        user.save()
        return user