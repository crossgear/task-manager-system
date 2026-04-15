from rest_framework import serializers
from .models import Project
from apps.tasks.serializers import TaskSerializer

class ProjectSerializer(serializers.ModelSerializer): # Serializer for creating and listing projects
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'members']
        read_only_fields = ['owner', 'created_at', 'members']

    def validate_name(self, value):# Ensure that the project name is unique for the user
        user = self.context['request'].user

        queryset = Project.objects.filter(owner=user, name=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "You already have a project with this name."
            )

        return value

    def create(self, validated_data): # Set the owner of the project to the current user
        validated_data['owner'] = self.context['request'].user
        project = super().create(validated_data)

        # Add the owner to the members of the project
        project.members.add(validated_data['owner'])
        
        return project

class ProjectDetailSerializer(ProjectSerializer): # Serializer for retrieving project details, including tasks and members
    tasks = TaskSerializer(many=True, read_only=True)
    members = serializers.StringRelatedField(many=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['tasks', 'members']

    

