# data_collector/serializers.py

from rest_framework import serializers
from .models import RawFile
from endoreg_db.models import AnonymizedFile

class RawFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawFile
        fields = '__all__'  # You can also list fields explicitly

class AnonymizedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymizedFile
        fields = '__all__'  # You can also list fields explicitly