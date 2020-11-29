from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class detailSerializer(serializers.Serializer):
    id = serializers.CharField(label='药品id')
