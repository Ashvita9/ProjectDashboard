# Project Dashboard - Architecture Overview

This document describes the architecture of the Project Dashboard application, a full-stack project management tool built with Vue.js and Django.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Vue.js)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Views     │  │ Components  │  │      Vuex Store         │ │
│  │ - Dashboard │  │ - TaskCard  │  │ - authModule            │ │
│  │ - Projects  │  │ - Navbar    │  │ - projectsModule        │ │
│  │ - Login     │  │ - Modals    │  │ - tasksModule           │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                          │                                      │
│                    ┌─────┴─────┐                                │
│                    │  Services │                                │
│                    │   (API)   │                                │
│                    └───────────┘                                │
└─────────────────────────────────────────────────────────────────┘
                           │
                     HTTP/REST API
                           │
┌─────────────────────────────────────────────────────────────────┐
│                     Backend (Django REST)                       │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │    authapp      │  │   projectapp    │                      │
│  │  - User model   │  │  - Project model│                      │
│  │  - Auth views   │  │  - Task model   │                      │
│  │  - Serializers  │  │  - CRUD views   │                      │
│  └─────────────────┘  └─────────────────┘                      │
│                          │                                      │
│                    ┌─────┴─────┐                                │
│                    │MongoEngine│                                │
│                    │   (ODM)   │                                │
│                    └───────────┘                                │
└─────────────────────────────────────────────────────────────────┘
                           │
                       MongoDB
```

## Frontend Structure

### Views
| View | Route | Purpose |
|------|-------|---------|
| `Dashboard.vue` | `/` | Overview with stats and recent activity |
| `Projects.vue` | `/projects` | List and manage all projects |
| `ProjectDetail.vue` | `/projects/:id` | Kanban board for a single project |
| `Login.vue` | `/login` | User authentication |
| `Register.vue` | `/register` | New user registration |

### Components
| Component | Purpose |
|-----------|---------|
| `Navbar.vue` | Top navigation with user menu |
| `NotificationCenter.vue` | Toast notifications system |
| `ProjectCard.vue` | Project display card |
| `ProjectModal.vue` | Create/Edit project form |
| `TaskCard.vue` | Task display card (draggable) |
| `TaskModal.vue` | Create/Edit task form |

### State Management (Vuex)
- **authModule**: User authentication state
- **projectsModule**: Projects CRUD and active project
- **tasksModule**: Tasks CRUD, grouped by project

### Services
- **api.js**: Axios instance with base configuration
- **auth.js**: Authentication API calls
- **project.js**: Project CRUD API calls
- **task.js**: Task CRUD API calls

## Backend Structure

### Apps
| App | Models | Purpose |
|-----|--------|---------|
| `authapp` | `User` | User management and authentication |
| `projectapp` | `Project`, `Task` | Project and task management |

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | User login |
| GET | `/api/projects/` | List user's projects |
| POST | `/api/projects/` | Create project |
| PUT | `/api/projects/` | Update project |
| DELETE | `/api/projects/` | Delete project |
| GET | `/api/tasks/` | List tasks (by project) |
| POST | `/api/tasks/` | Create task |
| PUT | `/api/tasks/` | Update task |
| PATCH | `/api/tasks/` | Partial update (status) |
| DELETE | `/api/tasks/` | Delete task |

## Database Schema (MongoDB)

### User Collection
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  password: String (hashed),
  created_at: DateTime
}
```

### Projects Collection
```javascript
{
  _id: ObjectId,
  name: String,
  description: String,
  owner: ObjectId (ref: User),
  start_date: DateTime,
  deployment_date: DateTime,
  created_at: DateTime
}
```

### Tasks Collection
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  project: ObjectId (ref: Project),
  status: "todo" | "in_progress" | "done",
  created_at: DateTime
}
```

## Key Design Decisions

1. **MongoDB + MongoEngine**: Chosen for flexibility with document structure and easy Python integration
2. **Vuex for State**: Centralized state enables reactive updates across components
3. **Component-based UI**: Reusable components (TaskCard, ProjectCard) for consistency
4. **Event Bus for Notifications**: Decoupled notification system using Vue instance
5. **Drag-and-drop with vuedraggable**: Library handles complex drag interactions in Kanban board
