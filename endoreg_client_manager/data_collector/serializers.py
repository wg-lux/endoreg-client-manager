# data_collector/serializers.py

from rest_framework import serializers
from .models import RawFile
from endoreg_db.models import AnonymizedFile, RawPdfFile, AnonymousImageAnnotation, DroppedName

class RawFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawFile
        fields = '__all__'  # Consider listing fields explicitly for better control

class ValidateAndSaveSerializer(serializers.Serializer):
    image_name = serializers.CharField(max_length=255)
    original_image_url = serializers.URLField(required=False, allow_blank=True)
    polyp_count = serializers.IntegerField()
    comments = serializers.CharField(max_length=500, allow_blank=True)
    gender = serializers.ListField(child=serializers.DictField())
    name_image_url = serializers.CharField(max_length=255)

class AnonymizedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymizedFile
        fields = '__all__'  # Consider listing fields explicitly

class AnonymousImageAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousImageAnnotation
        fields = '__all__'  # Consider listing fields explicitly

class DroppedNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DroppedName
        fields = ['id', 'name', 'gender', 'x', 'y', 'name_image_url', 'box_coordinates']

class AnonymousImageAnnotationSerializer(serializers.ModelSerializer):
    dropped_names = DroppedNameSerializer(many=True, required=False)

    class Meta:
        model = AnonymousImageAnnotation
        fields = [
            'id', 'label', 'image_name', 'original_image_url', 'polyp_count',
            'comments', 'gender', 'name_image_url', 'date_created', 'processed',
            'dropped_names'
        ]
        read_only_fields = ['id', 'date_created', 'processed']

    def create(self, validated_data):
        dropped_names_data = validated_data.pop('dropped_names', [])
        annotation = AnonymousImageAnnotation.objects.create(**validated_data)
        for dropped_name_data in dropped_names_data:
            DroppedName.objects.create(annotation=annotation, **dropped_name_data)
        return annotation