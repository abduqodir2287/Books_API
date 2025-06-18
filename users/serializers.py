from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"



