<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title">{{ isEditing ? 'Edit Task' : 'Create New Task' }}</h2>
      </div>

      <div v-if="errors.length" class="alert alert-error mb-20">
        <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title">Task Title</label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            required
            placeholder="Enter task title"
          />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea
            id="description"
            v-model="form.description"
            placeholder="Enter task description"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="status">Status</label>
          <select v-model="form.status" id="status">
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-outline" @click="close">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="isLoading">
            {{ isLoading ? 'Saving...' : 'Save Task' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskModal',
  props: {
    task: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      form: {
        title: '',
        description: '',
        status: 'todo'
      },
      isLoading: false,
      errors: []
    }
  },
  computed: {
    isEditing() {
      return !!this.task
    }
  },
  watch: {
    task: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.form = {
            title: newVal.title,
            description: newVal.description || '',
            status: newVal.status
          }
        }
      }
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    async handleSubmit() {
      this.errors = []

      if (!this.form.title.trim()) {
        this.errors.push('Task title is required')
        return
      }

      this.isLoading = true

      try {
        if (this.isEditing) {
          await this.$store.dispatch('tasks/updateTask', {
            taskId: this.task.id,
            title: this.form.title,
            description: this.form.description,
            status: this.form.status
          })
          this.$emit('updated')
        } else {
          await this.$store.dispatch('tasks/createTask', {
            projectId: this.$route.params.id,
            title: this.form.title,
            description: this.form.description,
            status: this.form.status
          })
          this.$emit('created')
        }
        this.close()
      } catch (error) {
        const errorMsg = error.response?.data?.message || 'Operation failed'
        this.errors.push(errorMsg)
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(42, 36, 33, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 10px;
  padding: 30px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 10px 40px rgba(42, 36, 33, 0.15);
}
</style>
