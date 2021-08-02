from rest_framework import serializers

class GetRepoSerializer(serializers.Serializer):
    repo_name = serializers.CharField()