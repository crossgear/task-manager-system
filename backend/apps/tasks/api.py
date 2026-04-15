from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .models import Project
from rest_framework import viewsets, permissions
from django.db.models import Q  

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return TaskSerializer

    def get_queryset(self):
        # Return only tasks that belong to projects owned by the user or where the user is a member
        user = self.request.user
        status = self.request.query_params.get('status')
        description = self.request.query_params.get('description')
        priority = self.request.query_params.get('priority')
        assigned_to = self.request.query_params.get('assigned_to')

        if user.is_anonymous: # If the user is not authenticated, return an empty queryset
            return Task.objects.none()

        queryset = Task.objects.filter(Q(project__owner=user) | Q(project__members=user)).distinct().select_related('project', 'assigned_to')

        if status:
            queryset = queryset.filter(status=status)

        if description:
            queryset = queryset.filter(description__icontains=description)

        if priority:
            queryset = queryset.filter(priority=priority)

        if assigned_to:
            queryset = queryset.filter(assigned_to=assigned_to)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        user = self.request.user

        if user not in project.members.all() and project.owner != user:
            raise PermissionDenied("User must be a member of the project to create tasks")
        
        serializer.save()

    def perform_update(self, serializer):
        project = serializer.validated_data.get('project', serializer.instance.project)
        user = self.request.user

        if user not in project.members.all() and project.owner != user:
            raise PermissionDenied("User must be a member of the project to update tasks")
        
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        project = instance.project
        user = request.user

        if user not in project.members.all() and project.owner != user:
            raise PermissionDenied("User must be a member of the project to delete tasks")

        self.perform_destroy(instance)

        return Response(
            {"detail": "Task deleted successfully"},
             status=200
         )