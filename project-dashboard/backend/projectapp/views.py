from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projectapp.models import Project, Task
from projectapp.serializers import ProjectSerializer, TaskSerializer
from authapp.models import User
from datetime import datetime

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
        start_date_str = request_data.get('start_date')
        deployment_date_str = request_data.get('deployment_date')
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
            # parse optional date strings (expecting ISO YYYY-MM-DD or full ISO)
            if start_date_str:
                try:
                    project.start_date = datetime.fromisoformat(start_date_str)
                except Exception:
                    return Response({'message': 'invalid start_date format, expected YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
            if deployment_date_str:
                try:
                    project.deployment_date = datetime.fromisoformat(deployment_date_str)
                except Exception:
                    return Response({'message': 'invalid deployment_date format, expected YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
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
        # Full update: allow clearing dates by providing empty/null, otherwise parse
        sd = request_data.get('start_date', None)
        if sd is None or sd == '':
            project.start_date = None
        else:
            try:
                project.start_date = datetime.fromisoformat(sd)
            except Exception:
                return Response({'message': 'invalid start_date format, expected YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        dd = request_data.get('deployment_date', None)
        if dd is None or dd == '':
            project.deployment_date = None
        else:
            try:
                project.deployment_date = datetime.fromisoformat(dd)
            except Exception:
                return Response({'message': 'invalid deployment_date format, expected YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
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
        if 'start_date' in request_data:
            sd = request_data.get('start_date')
            if sd in (None, ''):
                project.start_date = None
            else:
                try:
                    project.start_date = datetime.fromisoformat(sd)
                except Exception:
                    return Response({'message': 'invalid start_date format, expected YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
            changed = True
        if 'deployment_date' in request_data:
            dd = request_data.get('deployment_date')
            if dd in (None, ''):
                project.deployment_date = None
            else:
                try:
                    project.deployment_date = datetime.fromisoformat(dd)
                except Exception:
                    return Response({'message': 'invalid deployment_date format, expected YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
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
        user_id = request.GET.get('user_id')
        project_id = request.GET.get('project_id')
        if not user_id:
            return Response({'message': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not project_id:
            return Response({'message': 'project_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        tasks=Task.objects.filter(project=project_id).all()
        serialized_tasks = TaskSerializer(tasks, many=True).data
        return Response({"tasks": serialized_tasks}, status=status.HTTP_200_OK)
        
        

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
        request_status = request_data.get('status', 'todo')

        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response({'message': 'project not found'}, status=status.HTTP_404_NOT_FOUND)
        if str(project.owner.id) != str(request_user_id):
            return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        task = Task()
        try:
            task.title = title
            task.description = description
            task.project = project #foreign key 
            task.status = request_status
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
    