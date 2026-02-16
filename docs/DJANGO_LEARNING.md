# Django & Django REST Framework Learning Notes

This document captures key Django concepts learned while building the Project Dashboard backend.

## Django Basics

### Project Structure
```
backend/
├── manage.py           # CLI entry point
├── backend/            # Project configuration
│   ├── settings.py     # All settings
│   ├── urls.py         # Root URL config
│   └── wsgi.py         # WSGI application
├── authapp/            # Authentication app
└── projectapp/         # Business logic app
```

### Apps vs Projects
- **Project**: Configuration container (settings, root URLs)
- **App**: Reusable module with models, views, templates

**Lesson:** Keep apps focused - `authapp` for users, `projectapp` for projects/tasks.

### Settings Configuration
```python
# Environment-based settings
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

**Security note:** Never commit secrets. Use `.env` files and environment variables.

## Django REST Framework

### APIView Class
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProjectView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        return Response(
            {'projects': ProjectSerializer(projects, many=True).data},
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Why APIView over function views:**
- Better organization with class methods for HTTP verbs
- Built-in request parsing and response rendering
- Easy to extend with mixins

### Serializers
```python
from rest_framework_mongoengine.serializers import DocumentSerializer

class ProjectSerializer(DocumentSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner', 'created_at')
        read_only_fields = ('id', 'owner', 'created_at')
```

**Serializers handle:**
- Validation of incoming data
- Converting model instances to JSON
- Defining which fields are exposed

### Custom Validation
```python
class TaskSerializer(DocumentSerializer):
    def validate_status(self, value):
        valid_statuses = ['todo', 'in_progress', 'done']
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(valid_statuses)}"
            )
        return value
```

## MongoEngine (MongoDB ODM)

### Why MongoDB?
- Flexible schema for rapid prototyping
- Document structure maps well to JSON APIs
- No migrations needed for schema changes

### Document Models
```python
from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime

class Project(Document):
    meta = {
        'collection': 'projects',
        'db_alias': 'project_db'
    }
    name = StringField(required=True)
    description = StringField()
    owner = ReferenceField('User', required=True)
    created_at = DateTimeField(default=datetime.utcnow)
```

**Key concepts:**
- `meta` configures collection name and database alias
- Field types enforce schema at application level
- `ReferenceField` creates relationships between documents

### Querying
```python
# Get all projects for a user
projects = Project.objects(owner=user_id).all()

# Get single document
project = Project.objects(id=project_id).first()

# Update
project.update(name='New Name')

# Delete
project.delete()
```

### Connection Setup
```python
from mongoengine import connect

connect(
    db='project_dashboard_auth',
    alias='auth_db',
    host=CONNECTION_STRING
)
```

## URL Routing

### Project URLs
```python
# backend/urls.py
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('authapp.urls')),
    path('api/', include('projectapp.urls')),
]
```

### App URLs
```python
# projectapp/urls.py
from django.urls import path
from projectapp.views import ProjectView, TaskView

urlpatterns = [
    path('projects/', ProjectView.as_view()),
    path('tasks/', TaskView.as_view()),
]
```

## CORS Configuration

```python
# settings.py
INSTALLED_APPS = [
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be high in list
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]
```

**Why CORS matters:** Browsers block cross-origin requests by default. Frontend (port 8080) and backend (port 8000) are different origins.

## Error Handling Patterns

### Validation Helper
```python
def validate_keys(data, required_keys):
    missing = [key for key in required_keys if key not in data]
    if missing:
        return Response(
            {'message': 'missing required fields', 'missing_fields': missing},
            status=status.HTTP_400_BAD_REQUEST
        )
    return None

# Usage
def post(self, request):
    error = validate_keys(request.data, ['name', 'user_id'])
    if error:
        return error
    # Continue with valid data
```

### Try-Except Pattern
```python
def get(self, request):
    try:
        project = Project.objects(id=project_id).first()
        if not project:
            return Response(
                {'message': 'project not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({'project': ProjectSerializer(project).data})
    except Exception as e:
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

## HTTP Status Codes Used

| Code | Constant | When to Use |
|------|----------|-------------|
| 200 | `HTTP_200_OK` | Successful GET, PUT, PATCH |
| 201 | `HTTP_201_CREATED` | Successful POST (created) |
| 400 | `HTTP_400_BAD_REQUEST` | Invalid input data |
| 404 | `HTTP_404_NOT_FOUND` | Resource doesn't exist |
| 500 | `HTTP_500_INTERNAL_SERVER_ERROR` | Server error |

## Common Mistakes Made

1. **Forgetting CORS middleware order** - Must be before other middleware
2. **Not handling None returns** - `objects.first()` returns None if not found
3. **Mixing query params and body** - GET uses params, POST/PUT use body
4. **Date parsing without try-except** - Invalid dates crash the server
5. **Not validating ownership** - Always check user owns the resource

## Best Practices Adopted

1. **Consistent response format**: Always return `{message, data}` structure
2. **Input validation first**: Validate before any database operations
3. **Meaningful error messages**: Tell the client what went wrong
4. **Status codes matter**: Use appropriate codes for clients to handle
5. **Keep views thin**: Business logic in models or services, not views
