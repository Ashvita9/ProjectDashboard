<template>
  <div class="project-card">
    <div class="card-top">
      <div class="card-dot"></div>
      <div class="card-actions">
        <button class="btn-icon" @click="editProject" title="Edit">✎</button>
        <button class="btn-icon btn-icon-danger" @click="deleteProject" title="Delete">✕</button>
      </div>
    </div>

    <h3 class="card-name">{{ project.name }}</h3>
    <p class="card-desc">{{ project.description || 'No description' }}</p>

    <div class="card-footer">
      <span class="card-date">{{ formatDate(project.created_at) }}</span>
      <router-link :to="`/projects/${project.id}`" class="btn btn-outline btn-sm">Open →</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProjectCard',
  props: { project: { type: Object, required: true } },
  methods: {
    formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
    },
    editProject() { this.$emit('edit') },
    async deleteProject() {
      if (confirm('Are you sure you want to delete this project?')) {
        try {
          await this.$store.dispatch('projects/deleteProject', this.project.id)
          this.$emit('deleted')
        } catch (e) { alert('Failed to delete project') }
      }
    }
  }
}
</script>

<style scoped>
.project-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 22px;
  display: flex;
  flex-direction: column;
  transition: all 0.2s var(--ease);
}

.project-card:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-md);
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--accent);
}

.card-actions {
  display: flex;
  gap: 4px;
}

.btn-icon {
  width: 30px;
  height: 30px;
  padding: 0;
  border-radius: var(--radius-sm);
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s var(--ease);
  box-shadow: none;
}

.btn-icon:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.btn-icon-danger:hover {
  color: var(--color-danger);
  background: var(--color-danger-muted);
}

.card-name {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--text-primary);
}

.card-desc {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.5;
  flex: 1;
  margin-bottom: 18px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid var(--border);
}

.card-date {
  font-size: 12px;
  color: var(--text-muted);
}

.btn-sm {
  padding: 6px 14px;
  font-size: 12px;
}
</style>
