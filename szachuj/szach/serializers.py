from django.forms import widgets
from rest_framework import serializers
from szach.models import Szach


class SzachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Szach
        field = ('id', 'content', 'signature', 'stamp')