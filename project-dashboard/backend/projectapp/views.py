from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projectapp.models import Project, Task
from projectapp.serializers import ProjectSerializer, TaskSerializer
from authapp.models import User
from authapp.serializers import UserSerializer

def validate_keys(data, required_keys):
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
       return Response(
           {
            'message': 'missing required fields',
            'missing_fields': missing_keys
           },
        status=status.HTTP_400_BAD_REQUEST
    )
    return None

def _bool_value(value):
    return str(value).lower() in ("1", "true", "yes", "y", "t")

class ProjectView(APIView):
    def get(self, request):
        request_user_id = request.GET.get('user_id') 
        if not request_user_id:
            return Response({'message': 'user id is required'}, status=status.HTTP_400_BAD_REQUEST)
        userObj=User.objects(id=request_user_id).first()
        if not userObj:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        projects=Project.objects(owner=request_user_id).all()
        return Response(
            {
                "projects": ProjectSerializer(projects, many=True).data,
                "message": "projects fetched successfully"
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        request_data = request.data or {}
        request_user_id = request_data.get('user_id')       
        name = request_data.get('name')
        description = request_data.get('description')
        required_keys = ['user_id', 'name']
        validation_response = validate_keys(request_data, required_keys)
        if validation_response:
            return validation_response
        
        # Get the user object
        user = User.objects(id=request_user_id).first()
        if not user:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        project = Project()
        try:
            project.name = name
            project.description = description
            project.owner = user  # Assign User object, not string
            project.save()
            serialized_project = ProjectSerializer(project).data
        except Exception as e:
            return Response({'message': 'project creation failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(
            {
                "project": serialized_project,
                "message": "project created successfully"
            },
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        """Full update: requires `project_id`, `user_id`, and `name` (description optional)."""
        request_data = request.data or {}
        required_keys = ['project_id', 'user_id', 'name']
        validation_response = validate_keys(request_data, required_keys)
        if validation_response:
            return validation_response

        project_id = request_data.get('project_id')
        request_user_id = request_data.get('user_id')
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response({'message': 'project not found'}, status=status.HTTP_404_NOT_FOUND)
        if str(project.owner.id) != str(request_user_id):
            return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        project.name = request_data.get('name')
        project.description = request_data.get('description', '')
        try:
            project.save()
            serialized_project = ProjectSerializer(project).data
        except Exception as e:
            return Response({'message': 'project update failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"project": serialized_project, "message": "project updated"}, status=status.HTTP_200_OK)

    def patch(self, request):
        """Partial update: requires `project_id` and `user_id`. Only supplied fields are updated."""
        request_data = request.data or {}
        required_keys = ['project_id', 'user_id']
        validation_response = validate_keys(request_data, required_keys)
        if validation_response:
            return validation_response

        project_id = request_data.get('project_id')
        request_user_id = request_data.get('user_id')
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response({'message': 'project not found'}, status=status.HTTP_404_NOT_FOUND)
        if str(project.owner.id) != str(request_user_id):
            return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        changed = False
        if 'name' in request_data:
            project.name = request_data.get('name')
            changed = True
        if 'description' in request_data:
            project.description = request_data.get('description')
            changed = True

        if not changed:
            return Response({'message': 'no updatable fields provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project.save()
            serialized_project = ProjectSerializer(project).data
        except Exception as e:
            return Response({'message': 'project partial update failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"project": serialized_project, "message": "project partially updated"}, status=status.HTTP_200_OK)

    def delete(self, request):
        """Delete a project: requires `project_id` and `user_id`."""
        request_data = request.data or {}
        required_keys = ['project_id', 'user_id']
        validation_response = validate_keys(request_data, required_keys)
        if validation_response:
            return validation_response

        project_id = request_data.get('project_id')
        request_user_id = request_data.get('user_id')
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response({'message': 'project not found'}, status=status.HTTP_404_NOT_FOUND)
        if str(project.owner.id) != str(request_user_id):
            return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        try:
            project.delete()
        except Exception as e:
            return Response({'message': 'project deletion failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'project deleted'}, status=status.HTTP_200_OK)


class TaskView(APIView):
    def get(self, request):
        request_data = request.data or {}
        request_user_id = request_data.get('user_id')
        project_id = request_data.get('project_id')

        if project_id:
            project = Project.objects.filter(id=project_id).first()
            if not project:
                return Response({'message': 'project not found'}, status=status.HTTP_404_NOT_FOUND)
            if request_user_id and str(project.owner.id) != str(request_user_id):
                return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
            tasks = Task.objects.filter(project=project)
        elif request_user_id:
            # list tasks for all projects owned by user
            projects = Project.objects.filter(owner=request_user_id)
            tasks = Task.objects.filter(project__in=projects)
        else:
            # no filters provided, return all tasks
            tasks = Task.objects.all()

        response_data = TaskSerializer(tasks, many=True).data
        return Response({"result": response_data}, status=status.HTTP_200_OK)

    def post(self, request):
        request_data = request.data or {}
        required_keys = ['user_id', 'project_id', 'title']
        validation_response = validate_keys(request_data, required_keys)
        if validation_response:
            return validation_response

        request_user_id = request_data.get('user_id')
        project_id = request_data.get('project_id')
        title = request_data.get('title')
        description = request_data.get('description')

        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response({'message': 'project not found'}, status=status.HTTP_404_NOT_FOUND)
        if str(project.owner.id) != str(request_user_id):
            return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        task = Task()
        try:
            task.title = title
            task.description = description
            task.project = project
            task.status = request_data.get('status', task.status)
            task.save()
        except Exception as e:
            return Response({'message': 'task creation failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"task": TaskSerializer(task).data, "message": "task created successfully"}, status=status.HTTP_201_CREATED)

    def put(self, request):
        request_data = request.data or {}
        required_keys = ['task_id', 'user_id', 'title']
        validation_response = validate_keys(request_data, required_keys)
        if validation_response:
            return validation_response

        task_id = request_data.get('task_id')
        request_user_id = request_data.get('user_id')
        task = Task.objects.filter(id=task_id).first()
        if not task:
            return Response({'message': 'task not found'}, status=status.HTTP_404_NOT_FOUND)
        if str(task.project.owner.id) != str(request_user_id):
            return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        task.title = request_data.get('title')
        task.description = request_data.get('description', '')
        task.status = request_data.get('status', task.status)
        try:
            task.save()
        except Exception as e:
            return Response({'message': 'task update failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"task": TaskSerializer(task).data, "message": "task updated"}, status=status.HTTP_200_OK)

    def patch(self, request):
        request_data = request.data or {}
        required_keys = ['task_id', 'user_id']
        validation_response = validate_keys(request_data, required_keys)
        if validation_response:
            return validation_response

        task_id = request_data.get('task_id')
        request_user_id = request_data.get('user_id')
        task = Task.objects.filter(id=task_id).first()
        if not task:
            return Response({'message': 'task not found'}, status=status.HTTP_404_NOT_FOUND)
        if str(task.project.owner.id) != str(request_user_id):
            return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        changed = False
        if 'title' in request_data:
            task.title = request_data.get('title')
            changed = True
        if 'description' in request_data:
            task.description = request_data.get('description')
            changed = True
        if 'status' in request_data:
            task.status = request_data.get('status')
            changed = True

        if not changed:
            return Response({'message': 'no updatable fields provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task.save()
        except Exception as e:
            return Response({'message': 'task partial update failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"task": TaskSerializer(task).data, "message": "task partially updated"}, status=status.HTTP_200_OK)

    def delete(self, request):
        request_data = request.data or {}
        required_keys = ['task_id', 'user_id']
        validation_response = validate_keys(request_data, required_keys)
        if validation_response:
            return validation_response

        task_id = request_data.get('task_id')
        request_user_id = request_data.get('user_id')
        task = Task.objects.filter(id=task_id).first()
        if not task:
            return Response({'message': 'task not found'}, status=status.HTTP_404_NOT_FOUND)
        if str(task.project.owner.id) != str(request_user_id):
            return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        try:
            task.delete()
        except Exception as e:
            return Response({'message': 'task deletion failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'task deleted'}, status=status.HTTP_200_OK)
    