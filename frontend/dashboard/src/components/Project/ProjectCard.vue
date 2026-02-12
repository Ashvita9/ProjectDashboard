<template>
  <div class="project-card card">
    <div class="card-header flex-between">
      <h3 class="card-title">{{ project.name }}</h3>
      <div class="actions">
        <button class="btn-icon" @click="editProject" title="Edit">
          ✎
        </button>
        <button class="btn-icon btn-danger" @click="deleteProject" title="Delete">
          ✕
        </button>
      </div>
    </div>

    <p class="description">{{ project.description || 'No description' }}</p>

    <div class="project-meta">
      <span class="meta-item">
        <strong>Owner:</strong> {{ project.owner?.username || 'Unknown' }}
      </span>
      <span class="meta-item">
        <strong>Created:</strong> {{ formatDate(project.created_at) }}
      </span>
    </div>

    <router-link
      :to="`/projects/${project.id}`"
      class="btn btn-secondary mt-20"
    >
      View Tasks
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'ProjectCard',
  props: {
    project: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    editProject() {
      this.$emit('edit')
    },
    async deleteProject() {
      if (confirm('Are you sure you want to delete this project?')) {
        try {
          await this.$store.dispatch('projects/deleteProject', this.project.id)
          this.$emit('deleted')
        } catch (error) {
          alert('Failed to delete project')
        }
      }
    }
  }
}
</script>

<style scoped>
.project-card {
  display: flex;
  flex-direction: column;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: var(--clay-primary);
  transition: all 0.3s ease;
  padding: 4px 8px;
}

.btn-icon:hover {
  color: var(--clay-secondary);
  transform: scale(1.2);
}

.btn-icon.btn-danger {
  color: var(--clay-accent-danger);
}

.btn-icon.btn-danger:hover {
  color: #B76560;
}

.description {
  color: var(--clay-accent-info);
  margin: 10px 0;
  line-height: 1.5;
}

.project-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: var(--clay-accent-info);
  margin: 15px 0;
}

.meta-item {
  display: block;
}
</style>
