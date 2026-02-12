from projectapp.models import Project, Task
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class ProjectSerializer(DocumentSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner', 'created_at')
        read_only_fields = ('id','owner', 'created_at')

class TaskSerializer(DocumentSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'project', 'status', 'created_at')
        read_only_fields = ('id', 'project', 'created_at')

    def validate_status(self, value):
        if value not in ['todo', 'in_progress', 'done']:
            raise serializers.ValidationError("Status must be one of: 'todo', 'in_progress', 'done'")
        return value