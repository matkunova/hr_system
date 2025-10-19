from rest_framework import serializers
from .models import Worker


class WorkerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = (
            'id', 'first_name', 'middle_name',
            'last_name', 'position', 'is_active')


class WorkerDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Worker
        fields = '__all__'
        read_only_fields = ('hired_date', 'created_by', 'updated_at')