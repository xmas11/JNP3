from django.forms import widgets
from rest_framework import serializers
from szach.models import Szach


class SzachSerializer(serializers.Serializer):
    pk = serializers.Field()
    subject = serializers.CharField(required=True, max_length=1024)
    signature = serializers.CharField(required=True, max_length=128)

    def restore_object(self, attrs, instance=None):
        return Szach(**attrs)
