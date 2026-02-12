<template>
  <div class="dashboard">
    <div class="dashboard-header card">
      <h1>Welcome, {{ user?.username }}!</h1>
      <p>Your Project Management Dashboard</p>
    </div>

    <div class="dashboard-stats">
      <div class="stat-card card">
        <h3>Total Projects</h3>
        <div class="stat-value">{{ projectCount }}</div>
      </div>
      <div class="stat-card card">
        <h3>Total Tasks</h3>
        <div class="stat-value">{{ allTasks.length }}</div>
      </div>
      <div class="stat-card card">
        <h3>Completed Tasks</h3>
        <div class="stat-value">{{ completedTaskCount }}</div>
      </div>
      <div class="stat-card card">
        <h3>In Progress</h3>
        <div class="stat-value">{{ inProgressCount }}</div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="recent-projects">
        <h2>Recent Projects</h2>
        <router-link to="/projects" class="btn btn-secondary">View All Projects</router-link>
        
        <div v-if="isLoading" class="loading">
          <div class="spinner"></div>
        </div>

        <div v-else-if="recentProjects.length > 0" class="projects-grid">
          <div v-for="project in recentProjects" :key="project.id" class="project-preview card">
            <h3 class="project-name">{{ project.name }}</h3>
            <p class="project-desc">{{ project.description || 'No description' }}</p>
            <router-link :to="`/projects/${project.id}`" class="btn btn-primary">
              View Details
            </router-link>
          </div>
        </div>

        <div v-else class="empty-state">
          <p>No projects yet. Create your first project!</p>
          <router-link to="/projects" class="btn btn-primary">Create Project</router-link>
        </div>
      </div>

      <div class="recent-tasks">
        <h2>Recent Tasks</h2>
        
        <div v-if="recentTasks.length > 0" class="tasks-list">
          <div v-for="task in recentTasks" :key="task.id" class="task-item card">
            <div class="flex-between">
              <div>
                <h4>{{ task.title }}</h4>
                <span class="badge" :class="`badge-${task.status}`">
                  {{ statusLabel(task.status) }}
                </span>
              </div>
              <span class="project-tag">
                {{ getProjectName(task.project) }}
              </span>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <p>No tasks yet. Create your first task in a project!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  data() {
    return {
      isLoading: false
    }
  },
  computed: {
    ...mapState('auth', ['user']),
    ...mapGetters('projects', ['projectCount', 'allProjects']),
    ...mapGetters('tasks', ['completedTaskCount', 'allTasks']),
    recentProjects() {
      return this.allProjects.slice(0, 3)
    },
    recentTasks() {
      return this.allTasks.slice(0, 5)
    },
    inProgressCount() {
      return this.allTasks.filter(t => t.status === 'in_progress').length
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      this.isLoading = true
      try {
        const userId = this.$store.state.auth.userId
        await this.$store.dispatch('projects/fetchProjects', userId)
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      } finally {
        this.isLoading = false
      }
    },
    statusLabel(status) {
      const labels = {
        todo: 'To Do',
        in_progress: 'In Progress',
        done: 'Done'
      }
      return labels[status] || status
    },
    getProjectName(projectId) {
      const project = this.allProjects.find(p => p.id === projectId)
      return project ? project.name : 'Unknown'
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 30px;
}

.dashboard-header {
  margin-bottom: 30px;
  background: linear-gradient(135deg, var(--clay-primary) 0%, var(--clay-secondary) 100%);
  color: white;
}

.dashboard-header h1 {
  margin: 0 0 10px 0;
  font-size: 32px;
}

.dashboard-header p {
  margin: 0;
  opacity: 0.9;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  text-align: center;
  padding: 25px;
}

.stat-card h3 {
  margin: 0 0 15px 0;
  color: var(--clay-primary);
  font-size: 14px;
}

.stat-value {
  font-size: 40px;
  font-weight: bold;
  color: var(--clay-secondary);
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.recent-projects h2,
.recent-tasks h2 {
  color: var(--clay-primary);
  margin-top: 0;
  margin-bottom: 20px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.project-preview {
  display: flex;
  flex-direction: column;
}

.project-name {
  color: var(--clay-primary);
  margin: 0 0 10px 0;
}

.project-desc {
  color: var(--clay-accent-info);
  margin: 0 0 15px 0;
  font-size: 14px;
  flex-grow: 1;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}

.task-item {
  padding: 15px;
}

.task-item h4 {
  margin: 0 0 8px 0;
  color: var(--clay-primary);
}

.project-tag {
  font-size: 12px;
  background-color: var(--clay-light-bg-2);
  padding: 4px 8px;
  border-radius: 4px;
  color: var(--clay-accent-info);
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--clay-accent-info);
}

.loading {
  display: flex;
  justify-content: center;
  padding: 40px;
}

@media (max-width: 768px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }

  .dashboard {
    padding: 20px;
  }

  .dashboard-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
