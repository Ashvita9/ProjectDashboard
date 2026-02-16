# Project Dashboard Backend — Documentation Handbook

This README explains the backend code for the Project Dashboard (Django + Django REST Framework) in simple language. It shows where things live, what each file does, and includes short code snippets to make the ideas clear.

## Quick summary
- Where: `project-dashboard/backend/` — this is the Django project folder.
- Tech: Python, Django, Django REST Framework (DRF), SQLite (for development).
- Purpose: store projects, users, tasks and provide APIs that the frontend calls.

## How to run (developer)
1. Create a virtualenv and install requirements: `pip install -r requirements.txt`.
2. Run migrations: `python manage.py migrate`.
3. Start dev server: `python manage.py runserver`.

## Top-level layout and what each part does
- `manage.py` — command-line helper to run the server and tasks.
- `backend/` — Django project settings, URLs, WSGI/ASGI.
- `authapp/` — app responsible for authentication (users, tokens, serializers, views).
- `projectapp/` — app responsible for projects and tasks, their models, serializers, and views.

### `backend/settings.py` (what it handles)
- Central configuration: installed apps, middleware, database, REST framework settings, CORS.

Child explanation: `settings.py` is the control room — you turn features on and set where the data lives.

### `backend/urls.py`
- Top-level URL map. It says: if the incoming address starts with `/api/`, send it to the app's URL maps.

Example:
```py
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('authapp.urls')),
    path('api/projects/', include('projectapp.urls')),
]
```

### `authapp/` — authentication
- `models.py` — custom user model or relations (if present).
- `serializers.py` — convert Django models to JSON and back (for registration and login).
- `views.py` — endpoints for login, register, token refresh, profile.

Small example of a serializer:
```py
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
```

Child explanation: Serializers turn database rows into nice JSON that the frontend understands.

### `projectapp/` — projects and tasks
- `models.py` — Django models for `Project`, `Task`. Fields might include `title`, `description`, `status`, `assigned_to`, `due_date`.
- `serializers.py` — how to convert `Project` and `Task` to JSON.
- `views.py` — API endpoints to list projects, create a project, update tasks etc. These usually use DRF `ViewSet` or `APIView` classes.

Example view (very short):
```py
from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
```

Child explanation: A ViewSet is like a waiter who fetches projects from the database and gives them to the frontend.

## How data flows (simple)
1. Frontend calls `/api/projects/` (GET) using the Axios API helper.
2. Django's `ProjectViewSet` gets the request, asks the database for projects.
3. Serializer turns the projects into JSON.
4. The response is sent back to the frontend.

## Important files and purpose quick map
- `manage.py`: run tasks and server.
- `backend/settings.py`: global config.
- `backend/urls.py`: top-level URL routing.
- `authapp/`:
  - `models.py`: user related models.
  - `serializers.py`: user <-> JSON conversion.
  - `views.py`: login/register endpoints.
  - `urls.py`: mount auth endpoints.
- `projectapp/`:
  - `models.py`: `Project`, `Task` definitions.
  - `serializers.py`: convert to/from JSON.
  - `views.py`: endpoints for listing/creating/updating projects and tasks.
  - `urls.py`: mount project routes.

## Small examples to understand what's happening

Model example:
```py
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Serializer example:
```py
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
```

View example (function-based for clarity):
```py
@api_view(['GET'])
def project_list(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)
```

Child explanation: These three are the stack: Model (data), Serializer (translator), View (server endpoint).

## Running common tasks
- Create migrations: `python manage.py makemigrations`.
- Apply migrations: `python manage.py migrate`.
- Create superuser: `python manage.py createsuperuser`.
- Run server: `python manage.py runserver`.

## Debugging tips
- If database changes don't appear, run `migrate` and restart the server.
- Use Postman or curl to call endpoints and check responses.
- Check `backend/settings.py` for REST framework auth classes (Token vs JWT) to understand how tokens are validated.

## Where to add a new API endpoint (step-by-step)
1. Add or update a model in `projectapp/models.py`.
2. Add a serializer in `projectapp/serializers.py`.
3. Add a view (or ViewSet) in `projectapp/views.py`.
4. Add a route to `projectapp/urls.py` and include it from `backend/urls.py`.

---
This README is written to help new backend contributors understand the shape of the project and where to make changes. If you need a guided code walkthrough, open `projectapp/views.py` in the editor and look for functions or classes decorated with DRF decorators or subclasses of `ViewSet`.
