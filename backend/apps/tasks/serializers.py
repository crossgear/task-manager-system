from rest_framework import serializers
from .models import Task
from datetime import date

class TaskSerializer(serializers.ModelSerializer): # Serializer for Task model, includes validation for assigned user and due date
    class Meta:
        model = Task
        fields = '__all__'

    def validate(self, data):# Validate that assigned user is a member of the project and that completed tasks have a due date
        project = data.get('project') or self.instance.project if self.instance else None
        assigned_to = data.get('assigned_to') or self.instance.assigned_to if self.instance else None

        if assigned_to and project:
            if assigned_to not in project.members.all():
                raise serializers.ValidationError("Assigned user must be a member of the project.")

        status = data.get('status')
        due_date = data.get('due_date')
        
        if status == 'done' and not due_date:# Ensure that completed tasks have a due date
            raise serializers.ValidationError("Completed tasks must have a due date.")

        return data

    def validate_due_date(self, value):# Ensure that due date is not in the past
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value