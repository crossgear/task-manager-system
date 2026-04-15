from .models import Project
from .serializers import ProjectSerializer, ProjectDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, permissions
from django.db.models import Q

User = get_user_model()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return ProjectDetailSerializer
        return ProjectSerializer

    def get_queryset(self):
        # Return only projects owned by the user or where the user is a member
        user = self.request.user

        if user.is_anonymous: # If the user is not authenticated, return an empty queryset
            return Project.objects.none()

        return Project.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct().prefetch_related('members', 'tasks')
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.owner != request.user:
            raise PermissionDenied("Only owner can delete this project")

        self.perform_destroy(instance)

        return Response(
            {"detail": "Project deleted successfully"},
            status=200
        )

    @action(detail=True, methods=['get','post'], permission_classes=[permissions.IsAuthenticated], url_path='tasks')
    def tasks(self, request, pk=None):
        #print("METHOD:", request.method)
        project = self.get_object()

        if request.method == 'GET': # List tasks of the project
            tasks = project.tasks.all()

            #filters

            if status_param := request.query_params.get('status'):
                tasks = tasks.filter(status=status_param)
            
            if priority_param := request.query_params.get('priority'):
                tasks = tasks.filter(priority=priority_param)

            if assigned_to_param := request.query_params.get('assigned_to'):
                tasks = tasks.filter(assigned_to__id=assigned_to_param)

            data = [
            {
                'id': t.id,
                'title': t.title,
                'description': t.description,
                'status': t.status,
                'priority': t.priority,
                'assigned_to': t.assigned_to_id
            }
            for t in tasks
        ]

            return Response(data)

        elif request.method == 'POST': # Create a new task in the project
            title = request.data.get('title')

            if not title:
                return Response({'detail': 'Title is required.'}, status=status.HTTP_400_BAD_REQUEST)

            task = project.tasks.create(title=title)
            return Response({'id': task.id, 'title': task.title}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='members-list')
    def list_members(self, request, pk=None): # Get members of the project
        project = self.get_object()
        members = project.members.all()
        member_data = [{'id': member.id, 'username': member.username} for member in members]
        return Response(member_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def members(self, request, pk=None): # Add a member to the project
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user_to_add = User.objects.get(id=user_id)
            if user_to_add in project.members.all():
                return Response(
                        {"detail": "User already in project"},
                        status=status.HTTP_400_BAD_REQUEST
                )
            if user_to_add == project.owner:
                return Response(
                        {"detail": "Owner is already part of the project"},
                        status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        project.members.add(user_to_add)
        return Response({'detail': f'{user_to_add.username} added to the project.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'], url_path='members/(?P<user_id>[^/.]+)')
    def remove_member(self, request, pk=None, user_id=None):
        project = self.get_object()

        if request.user != project.owner:
            return Response(
                {"detail": "Only owner can remove members"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if user not in project.members.all():
            return Response(
                {"detail": "User is not a member"},
                status=status.HTTP_400_BAD_REQUEST
            )

        project.members.remove(user)
        project.refresh_from_db()

        return Response(
            {"detail": "User removed from project"},
            status=status.HTTP_200_OK
        )