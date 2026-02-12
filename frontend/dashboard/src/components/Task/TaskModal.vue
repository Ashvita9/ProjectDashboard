<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title">{{ isEditing ? 'Edit Task' : 'New Task' }}</h2>
      </div>

      <div v-if="errors.length" class="alert alert-error">
        <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title">Title</label>
          <input id="title" v-model="form.title" type="text" required placeholder="What needs to be done?" />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea id="description" v-model="form.description" placeholder="Add more details…"></textarea>
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
            {{ isLoading ? 'Saving…' : isEditing ? 'Save Changes' : 'Create Task' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskModal',
  props: { task: { type: Object, default: null } },
  data() {
    return { form: { title: '', description: '', status: 'todo' }, isLoading: false, errors: [] }
  },
  computed: { isEditing() { return !!this.task } },
  watch: {
    task: {
      immediate: true,
      handler(v) {
        if (v) this.form = { title: v.title, description: v.description || '', status: v.status }
      }
    }
  },
  methods: {
    close() { this.$emit('close') },
    async handleSubmit() {
      this.errors = []
      if (!this.form.title.trim()) { this.errors.push('Task title is required'); return }
      this.isLoading = true
      try {
        if (this.isEditing) {
          await this.$store.dispatch('tasks/updateTask', {
            taskId: this.task.id, title: this.form.title,
            description: this.form.description, status: this.form.status
          })
          this.$emit('updated')
        } else {
          await this.$store.dispatch('tasks/createTask', {
            projectId: this.$route.params.id, title: this.form.title,
            description: this.form.description, status: this.form.status
          })
          this.$emit('created')
        }
        this.close()
      } catch (e) {
        this.errors.push(e.response?.data?.message || 'Operation failed')
      } finally { this.isLoading = false }
    }
  }
}
</script>

<style scoped>
/* Inherits global modal styles from clay-theme.css */
</style>
