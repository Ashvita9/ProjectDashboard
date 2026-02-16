<template>
  <div class="dashboard">
    <!-- Header -->
    <div class="dash-header">
      <div>
        <h1 class="greeting">Welcome back<span v-if="user">, {{ user.username }}</span></h1>
        <p class="sub">Track your projects and tasks in one place.</p>
      </div>
      <div class="header-actions">
        <router-link to="/projects" class="btn btn-primary">+ New Project</router-link>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-row">
      <div class="stat-tile">
        <span class="stat-label">Projects</span>
        <span class="stat-number">{{ projectCount }}</span>
      </div>
      <div class="stat-tile">
        <span class="stat-label">Total Tasks</span>
        <span class="stat-number">{{ allTasks.length }}</span>
      </div>
      <div class="stat-tile stat-accent">
        <span class="stat-label">In Progress</span>
        <span class="stat-number">{{ inProgressCount }}</span>
      </div>
      <div class="stat-tile stat-green">
        <span class="stat-label">Completed</span>
        <span class="stat-number">{{ completedTaskCount }}</span>
      </div>
    </div>

    <!-- Content -->
    <div class="dash-grid">
      <!-- Projects -->
      <section class="panel">
        <div class="panel-header">
          <h2>Recent Projects</h2>
          <router-link to="/projects" class="link-subtle">View all →</router-link>
        </div>

        <div v-if="isLoading" class="panel-empty">
          <div class="spinner"></div>
        </div>

        <div v-else-if="recentProjects.length > 0" class="project-table">
          <router-link v-for="project in recentProjects" :key="project.id" :to="`/projects/${project.id}`"
            class="project-row">
            <div class="row-leading">
              <span class="dot"></span>
              <div>
                <span class="row-title">{{ project.name }}</span>
                <span class="row-sub">{{ (project.description || 'No description').substring(0, 50) }}</span>
              </div>
            </div>
            <span class="row-date">{{ formatDate(project.created_at) }}</span>
          </router-link>
        </div>

        <div v-else class="panel-empty">
          <p>No projects yet.</p>
          <router-link to="/projects" class="btn btn-outline">Create one</router-link>
        </div>
      </section>

      <!-- Activity -->
      <section class="panel">
        <div class="panel-header">
          <h2>Activity</h2>
        </div>

        <div v-if="recentTasks.length > 0" class="activity-list">
          <div v-for="task in recentTasks" :key="task.id" class="activity-item">
            <span class="status-dot" :class="`dot-${task.status}`"></span>
            <div class="activity-body">
              <span class="activity-title">{{ task.title }}</span>
              <span class="activity-meta">{{ getProjectName(task.project) }} · {{ formatDate(task.created_at) }}</span>
            </div>
            <span class="badge" :class="`badge-${task.status}`">{{ statusLabel(task.status) }}</span>
          </div>
        </div>

        <div v-else class="panel-empty">
          <p>No recent activity.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  data() {
    return { isLoading: false, error: null }
  },
  computed: {
    ...mapState('auth', ['user']),
    ...mapGetters('projects', ['projectCount', 'allProjects']),
    ...mapGetters('tasks', ['completedTaskCount', 'allTasks']),
    recentProjects() { return [...this.allProjects].slice(0, 5) },
    recentTasks() { return [...this.allTasks].slice(0, 6) },
    inProgressCount() { return this.allTasks.filter(t => t.status === 'in_progress').length }
  },
  mounted() { this.loadData() },
  methods: {
    async loadData() {
      this.isLoading = true
      try {
        const userId = this.$store.state.auth.userId
        await this.$store.dispatch('projects/fetchProjects', userId)
      } catch (e) {
        this.error = e.response?.data?.message || 'Failed to load data'
      } finally {
        this.isLoading = false
      }
    },
    statusLabel(s) {
      return { todo: 'To Do', in_progress: 'Working', done: 'Done' }[s] || s
    },
    getProjectName(id) {
      const p = this.allProjects.find(p => p.id === id)
      return p ? p.name : '—'
    },
    formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 24px;
}

/* Header */
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
  gap: 16px;
}

.greeting {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.sub {
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 4px;
}

/* Stats */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-tile {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: border-color 0.2s var(--ease);
}

.stat-tile:hover {
  border-color: var(--border-strong);
}

.stat-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
}

.stat-number {
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text-primary);
}

.stat-accent .stat-number {
  color: var(--color-warning);
}

.stat-green .stat-number {
  color: var(--color-success);
}

/* Grid */
.dash-grid {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 20px;
  align-items: start;
}

/* Panel */
.panel {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 22px;
  border-bottom: 1px solid var(--border);
}

.panel-header h2 {
  font-size: 15px;
  font-weight: 700;
}

.link-subtle {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}

.link-subtle:hover {
  color: var(--accent-light);
}

/* Project Rows */
.project-table {
  display: flex;
  flex-direction: column;
}

.project-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 22px;
  text-decoration: none;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border);
  transition: background 0.12s var(--ease);
}

.project-row:last-child {
  border-bottom: none;
}

.project-row:hover {
  background: var(--bg-hover);
}

.row-leading {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent);
  flex-shrink: 0;
}

.row-title {
  display: block;
  font-weight: 600;
  font-size: 14px;
}

.row-sub {
  display: block;
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.row-date {
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
}

/* Activity */
.activity-list {
  display: flex;
  flex-direction: column;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 22px;
  border-bottom: 1px solid var(--border);
}

.activity-item:last-child {
  border-bottom: none;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot-todo {
  background: var(--text-muted);
}

.dot-in_progress {
  background: var(--color-warning);
}

.dot-done {
  background: var(--color-success);
}

.activity-body {
  flex: 1;
  min-width: 0;
}

.activity-title {
  display: block;
  font-size: 13px;
  font-weight: 600;
}

.activity-meta {
  display: block;
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

.panel-empty {
  padding: 40px 22px;
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
}

/* Responsive */
@media (max-width: 900px) {
  .dash-grid {
    grid-template-columns: 1fr;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-row {
    grid-template-columns: 1fr 1fr;
  }

  .dash-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
