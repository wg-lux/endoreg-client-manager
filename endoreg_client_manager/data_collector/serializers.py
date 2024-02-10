# data_collector/serializers.py

from rest_framework import serializers
from .models import RawFile

class RawFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawFile
        fields = '__all__'  # You can also list fields explicitly
