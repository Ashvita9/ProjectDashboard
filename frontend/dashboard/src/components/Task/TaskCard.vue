<template>
  <div class="task-card">
    <div class="task-top">
      <h4 class="task-title">{{ task.title }}</h4>
      <div class="task-actions">
        <button class="btn-icon" @click.stop="editTask" title="Edit">✎</button>
        <button class="btn-icon btn-icon-danger" @click.stop="deleteTask" title="Delete">✕</button>
      </div>
    </div>

    <p v-if="task.description" class="task-desc">{{ task.description }}</p>

    <div class="task-bottom">
      <span class="badge" :class="`badge-${task.status}`">{{ statusLabel }}</span>
      <span class="task-date">{{ formatDate(task.created_at) }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskCard',
  props: {
    task: { type: Object, required: true }
  },
  computed: {
    statusLabel() {
      return { todo: 'To Do', in_progress: 'In Progress', done: 'Done' }[this.task.status] || this.task.status
    }
  },
  methods: {
    formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    },
    editTask() { this.$emit('edit') },
    async deleteTask() {
      if (confirm('Delete this task?')) {
        try {
          await this.$store.dispatch('tasks/deleteTask', this.task.id)
          this.$emit('deleted')
        } catch (e) { alert('Failed to delete task') }
      }
    }
  }
}
</script>

<style scoped>
.task-card {
  display: block;
  min-height: 64px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  padding: 14px 16px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.task-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.task-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px;
}

.task-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  margin: 0;
}

.task-actions {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.15s ease;
}

.task-card:hover .task-actions {
  opacity: 1;
}

.btn-icon {
  width: 28px;
  height: 28px;
  padding: 0;
  border-radius: 6px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 13px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
  box-shadow: none;
}

.btn-icon:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
  transform: scale(1.1);
}

.btn-icon-danger:hover {
  color: var(--color-danger);
  background: var(--color-danger-muted);
}

.task-desc {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
  margin-bottom: 10px;
}

.task-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-date {
  font-size: 11px;
  color: var(--text-muted);
}
</style>
