from rest_framework.serializers import Serializer, CharField, BooleanField


class UserAPISerializer(Serializer):
    username = CharField()
    is_superuser = BooleanField()
