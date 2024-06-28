from rest_framework import serializers

class MaterialSerializer(serializers.Serializer):
    material = serializers.CharField(max_length=100)
    percentage = serializers.FloatField()

class EmissionInputSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    materials = serializers.ListField(child=MaterialSerializer())
