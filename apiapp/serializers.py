from rest_framework import serializers

class MaterialSerializer(serializers.Serializer):
    material = serializers.CharField(max_length=100)
    percentage = serializers.FloatField()

class EmissionInputSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    materials = serializers.ListField(child=MaterialSerializer())
class DigitalProductSerializer(serializers.Serializer):
    product_category = serializers.ChoiceField(choices=[
        ('Ebook', 'Ebook'),
        ('Music', 'Music'),
        ('Movies', 'Movies'),
        ('Games', 'Games'),
        ('TV Serial', 'TV Serial'),
        ('App Software', 'App Software'),
        ('Stage Art', 'Stage Art'),
    ])
    product_type = serializers.CharField()