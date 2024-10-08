from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=45, required=True)
    description = serializers.CharField(max_length=45, required=True)
    price = serializers.DecimalField(decimal_places=2, max_digits=62, required=True)
    rent_fee = serializers.DecimalField(decimal_places=2, max_digits=62, required=True)
    release_year = serializers.DateField(required=True)
    author_id = serializers.IntegerField( required=True)
    quantity = serializers.IntegerField( required=True)
    category = serializers.CharField(max_length=45, required=True)