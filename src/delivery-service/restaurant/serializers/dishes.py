from rest_framework import serializers


class DishSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	name = serializers.CharField(max_length=100)
	price = serializers.FloatField()
	is_available = serializers.BooleanField()
