<template>
  <div class="task-card card">
    <div class="card-header flex-between">
      <div>
        <h4 class="task-title">{{ task.title }}</h4>
        <span class="badge" :class="`badge-${task.status}`">
          {{ statusLabel }}
        </span>
      </div>
      <div class="actions">
        <button class="btn-icon" @click="editTask" title="Edit">
          ✎
        </button>
        <button class="btn-icon btn-danger" @click="deleteTask" title="Delete">
          ✕
        </button>
      </div>
    </div>

    <p v-if="task.description" class="description">{{ task.description }}</p>

    <div class="task-meta">
      <span class="meta-item">
        <strong>Created:</strong> {{ formatDate(task.created_at) }}
      </span>
    </div>

    <div v-if="!viewOnly" class="task-actions">
      <select
        :value="task.status"
        @change="changeStatus"
        class="status-select"
      >
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
    task: {
      type: Object,
      required: true
    },
    viewOnly: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    statusLabel() {
      const labels = {
        todo: 'To Do',
        in_progress: 'In Progress',
        done: 'Done'
      }
      return labels[this.task.status] || this.task.status
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
    editTask() {
      this.$emit('edit')
    },
    async deleteTask() {
      if (confirm('Are you sure you want to delete this task?')) {
        try {
          await this.$store.dispatch('tasks/deleteTask', this.task.id)
          this.$emit('deleted')
        } catch (error) {
          alert('Failed to delete task')
        }
      }
    },
    async changeStatus(event) {
      const newStatus = event.target.value
      try {
        await this.$store.dispatch('tasks/updateTask', {
          taskId: this.task.id,
          title: this.task.title,
          description: this.task.description,
          status: newStatus
        })
        this.$emit('status-changed', newStatus)
      } catch (error) {
        alert('Failed to update task status')
      }
    }
  }
}
</script>

<style scoped>
.task-card {
  border-left: 4px solid var(--clay-secondary);
}

.task-title {
  margin: 0;
  color: var(--clay-primary);
  font-size: 16px;
}

.description {
  color: var(--clay-accent-info);
  margin: 10px 0;
  line-height: 1.5;
  font-size: 14px;
}

.task-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: var(--clay-accent-info);
  margin: 10px 0;
}

.meta-item {
  display: block;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 16px;
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

.task-actions {
  margin-top: 15px;
}

.status-select {
  padding: 6px 10px;
  border: 1px solid var(--clay-border);
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}
</style>
