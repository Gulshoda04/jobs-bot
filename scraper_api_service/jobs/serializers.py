from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'url', 'location', 'posted_at', 'scraped_at']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title bo‘sh bo‘lishi mumkin emas")
        return value