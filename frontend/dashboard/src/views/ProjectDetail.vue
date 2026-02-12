<template>
  <div class="project-detail">
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
    </div>

    <template v-else-if="activeProject">
      <div class="detail-header">
        <router-link to="/projects" class="btn btn-outline">← Back to Projects</router-link>
        <div class="header-content">
          <h1>{{ activeProject.name }}</h1>
          <p v-if="activeProject.description" class="description">
            {{ activeProject.description }}
          </p>
        </div>
        <button class="btn btn-secondary" @click="editProject">Edit Project</button>
      </div>

      <div class="tasks-section">
        <div class="section-header">
          <h2>Project Tasks</h2>
          <button class="btn btn-primary" @click="showCreateTaskModal = true">
            + Add Task
          </button>
        </div>

        <div v-if="errors.length" class="alert alert-error">
          <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
        </div>

        <div class="tasks-by-status">
          <div class="status-column">
            <h3 class="status-title">
              To Do
              <span class="status-count">{{ todoTasks.length }}</span>
            </h3>
            <div class="tasks-list">
              <TaskCard
                v-for="task in todoTasks"
                :key="task.id"
                :task="task"
                @edit="editTask(task)"
                @deleted="loadProjectTasks"
                @status-changed="loadProjectTasks"
              />
            </div>
          </div>

          <div class="status-column">
            <h3 class="status-title">
              In Progress
              <span class="status-count">{{ inProgressTasks.length }}</span>
            </h3>
            <div class="tasks-list">
              <TaskCard
                v-for="task in inProgressTasks"
                :key="task.id"
                :task="task"
                @edit="editTask(task)"
                @deleted="loadProjectTasks"
                @status-changed="loadProjectTasks"
              />
            </div>
          </div>

          <div class="status-column">
            <h3 class="status-title">
              Done
              <span class="status-count">{{ doneTasks.length }}</span>
            </h3>
            <div class="tasks-list">
              <TaskCard
                v-for="task in doneTasks"
                :key="task.id"
                :task="task"
                @edit="editTask(task)"
                @deleted="loadProjectTasks"
                @status-changed="loadProjectTasks"
              />
            </div>
          </div>
        </div>

        <div v-if="tasksByProjectId.length === 0" class="empty-state">
          <p>No tasks yet. Create your first task!</p>
          <button class="btn btn-primary" @click="showCreateTaskModal = true">
            Create Task
          </button>
        </div>
      </div>

      <!-- Project Edit Modal -->
      <ProjectModal
        v-if="showEditProjectModal"
        :project="activeProject"
        @close="showEditProjectModal = false"
        @updated="handleProjectUpdated"
      />

      <!-- Task Create/Edit Modal -->
      <TaskModal
        v-if="showCreateTaskModal || showEditTaskModal"
        :task="editingTask"
        @close="closeTaskModal"
        @created="handleTaskCreated"
        @updated="handleTaskUpdated"
      />
    </template>

    <div v-else class="error-container">
      <p>Project not found.</p>
      <router-link to="/projects" class="btn btn-primary">Back to Projects</router-link>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import TaskCard from '@/components/Task/TaskCard.vue'
import TaskModal from '@/components/Task/TaskModal.vue'
import ProjectModal from '@/components/Project/ProjectModal.vue'

export default {
  name: 'ProjectDetail',
  components: {
    TaskCard,
    TaskModal,
    ProjectModal
  },
  data() {
    return {
      isLoading: false,
      errors: [],
      showCreateTaskModal: false,
      showEditTaskModal: false,
      showEditProjectModal: false,
      editingTask: null
    }
  },
  computed: {
    ...mapState('projects', ['activeProject']),
    projectId() {
      return this.$route.params.id
    },
    tasksByProjectId() {
      const projectId = this.projectId
      const allTasks = this.$store.state.tasks.tasksByProject[projectId] || []
      return allTasks
    },
    todoTasks() {
      return this.tasksByProjectId.filter(t => t.status === 'todo')
    },
    inProgressTasks() {
      return this.tasksByProjectId.filter(t => t.status === 'in_progress')
    },
    doneTasks() {
      return this.tasksByProjectId.filter(t => t.status === 'done')
    }
  },
  watch: {
    '$route.params.id': {
      immediate: true,
      handler(newId) {
        this.loadProjectData(newId)
      }
    }
  },
  methods: {
    async loadProjectData(projectId) {
      this.isLoading = true
      this.errors = []

      try {
        const userId = this.$store.state.auth.userId
        
        // Fetch all projects if not already loaded
        if (this.$store.getters['projects/projectCount'] === 0) {
          await this.$store.dispatch('projects/fetchProjects', userId)
        }

        // Find and set the active project
        const project = this.$store.getters['projects/getProjectById'](projectId)
        if (project) {
          this.$store.dispatch('projects/setActiveProject', project)
        }

        // Load tasks for this project
        await this.loadProjectTasks()
      } catch (error) {
        const errorMsg = error.response?.data?.message || 'Failed to load project'
        this.errors.push(errorMsg)
      } finally {
        this.isLoading = false
      }
    },
    async loadProjectTasks() {
      try {
        await this.$store.dispatch('tasks/fetchTasksByProject', this.projectId)
      } catch (error) {
        const errorMsg = error.response?.data?.message || 'Failed to load tasks'
        this.errors.push(errorMsg)
      }
    },
    editProject() {
      this.showEditProjectModal = true
    },
    editTask(task) {
      this.editingTask = task
      this.showEditTaskModal = true
    },
    closeTaskModal() {
      this.showCreateTaskModal = false
      this.showEditTaskModal = false
      this.editingTask = null
    },
    handleProjectUpdated() {
      this.showEditProjectModal = false
      this.errors = []
    },
    handleTaskCreated() {
      this.closeTaskModal()
      this.loadProjectTasks()
    },
    handleTaskUpdated() {
      this.closeTaskModal()
      this.loadProjectTasks()
    }
  }
}
</script>

<style scoped>
.project-detail {
  padding: 30px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 40px;
  padding: 25px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(87, 73, 63, 0.1);
}

.header-content {
  flex-grow: 1;
}

.detail-header h1 {
  color: var(--clay-primary);
  margin: 0 0 10px 0;
}

.description {
  color: var(--clay-accent-info);
  margin: 0;
  line-height: 1.5;
}

.tasks-section {
  margin-top: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.section-header h2 {
  color: var(--clay-primary);
  margin: 0;
}

.tasks-by-status {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
}

.status-column {
  background-color: var(--clay-light-bg);
  border-radius: 8px;
  padding: 20px;
  min-height: 300px;
}

.status-title {
  color: var(--clay-primary);
  margin: 0 0 20px 0;
  font-size: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-count {
  background-color: var(--clay-secondary);
  color: white;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background-color: var(--clay-light-bg);
  border-radius: 8px;
}

.empty-state p {
  color: var(--clay-accent-info);
  margin-bottom: 20px;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: 60px;
}

.error-container {
  text-align: center;
  padding: 60px 20px;
}

@media (max-width: 768px) {
  .project-detail {
    padding: 20px;
  }

  .detail-header {
    flex-direction: column;
  }

  .tasks-by-status {
    grid-template-columns: 1fr;
  }
}
</style>
