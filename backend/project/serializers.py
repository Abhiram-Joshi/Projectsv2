from rest_framework import serializers

class GetRepoSerializer(serializers.Serializer):
    repo_name = serializers.CharField()

class UploadImageSerializer(serializers.Serializer):
    repo_name = serializers.CharField()
    repo_thumbnail = serializers.CharField()