from rest_framework import serializers
from myapp.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'fullname', 'phone', 'address')

