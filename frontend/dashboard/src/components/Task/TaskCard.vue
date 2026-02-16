<template>
  <div class="task-card">
    <div class="task-top">
      <h4 class="task-title">{{ task.title }}</h4>
      <div class="task-actions">
        <button class="btn-icon" @click="editTask" title="Edit">✎</button>
        <button class="btn-icon btn-icon-danger" @click="deleteTask" title="Delete">✕</button>
      </div>
    </div>

    <p v-if="task.description" class="task-desc">{{ task.description }}</p>

    <div class="task-bottom">
      <span class="badge" :class="`badge-${task.status}`">{{ statusLabel }}</span>
      <span class="task-date">{{ formatDate(task.created_at) }}</span>
    </div>

    <div v-if="!viewOnly" class="task-status-change">
      <select :value="task.status" @change="changeStatus" class="status-select">
        <option value="todo">To Do</option>
        <option value="in_progress">In Progress</option>
        <option value="done">Done</option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskCard',
  props: {
    task: { type: Object, required: true },
    viewOnly: { type: Boolean, default: false }
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
    // Drag handled by vuedraggable; keep handlers removed to avoid native-drag conflicts.
    async deleteTask() {
      if (confirm('Delete this task?')) {
        try {
          await this.$store.dispatch('tasks/deleteTask', this.task.id)
          this.$emit('deleted')
        } catch (e) { alert('Failed to delete task') }
      }
    },
    async changeStatus(event) {
      try {
        await this.$store.dispatch('tasks/updateTask', {
          taskId: this.task.id, title: this.task.title,
          description: this.task.description, status: event.target.value
        })
        this.$emit('status-changed', event.target.value)
      } catch (e) { alert('Failed to update status') }
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
  cursor: grab;
  transition: all 0.15s var(--ease);
}

.task-card:active {
  cursor: grabbing;
}

.task-card:hover {
  border-color: var(--border-strong);
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
  transition: all 0.12s var(--ease);
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

.task-status-change {
  margin-top: 10px;
}

.status-select {
  width: 100%;
  padding: 6px 10px;
  background: var(--bg-primary);
  border: 1px solid var(--border-strong);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 12px;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  cursor: pointer;
  outline: none;
  transition: border-color 0.15s var(--ease);
}

.status-select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-muted);
}
</style>
