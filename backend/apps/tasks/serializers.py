from django.utils import timezone
from rest_framework import serializers

from apps.employees.models import Employee
from apps.employees.serializers import EmployeeSerializer
from apps.projects.models import Project
from apps.projects.serializers import ProjectSerializer

from .models import Comment, Task


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.filter(is_active=True))
    project_detail = ProjectSerializer(source='project', read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(status=Employee.Status.ACTIVE),
        allow_null=True,
        required=False,
    )
    assigned_to_detail = EmployeeSerializer(source='assigned_to', read_only=True)
    comments_count = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'project',
            'project_detail',
            'assigned_to',
            'assigned_to_detail',
            'title',
            'description',
            'due_date',
            'priority',
            'status',
            'comments_count',
            'is_overdue',
            'created_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'project_detail',
            'assigned_to_detail',
            'comments_count',
            'is_overdue',
            'created_by',
            'created_at',
            'updated_at',
        ]

    def get_comments_count(self, obj: Task) -> int:
        return obj.comments.count()

    def get_is_overdue(self, obj: Task) -> bool:
        return obj.status != Task.Status.COMPLETED and obj.due_date < timezone.localdate()

    def validate_title(self, value: str) -> str:
        title = ' '.join(value.strip().split())
        if len(title) < 2:
            raise serializers.ValidationError('Task title must contain at least 2 characters.')
        return title

    def validate_due_date(self, value):
        if value < timezone.localdate():
            raise serializers.ValidationError('Due date cannot be in the past.')
        return value


class TaskAssignSerializer(serializers.Serializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(status=Employee.Status.ACTIVE),
        allow_null=True,
    )


class TaskStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Task.Status.choices)


class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'author_email', 'message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'task', 'author', 'author_email', 'created_at', 'updated_at']

    def validate_message(self, value: str) -> str:
        message = value.strip()
        if len(message) < 2:
            raise serializers.ValidationError('Comment message must contain at least 2 characters.')
        return message

