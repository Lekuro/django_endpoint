from rest_framework import serializers


class ParaphraseSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    tree = serializers.CharField(required=True)
    limit = serializers.IntegerField(default=20, required=False)
