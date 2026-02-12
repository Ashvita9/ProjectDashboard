<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title">{{ isEditing ? 'Edit Project' : 'New Project' }}</h2>
      </div>

      <div v-if="errors.length" class="alert alert-error">
        <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="name">Project Name</label>
          <input id="name" v-model="form.name" type="text" required placeholder="e.g. Website Redesign" />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea id="description" v-model="form.description" placeholder="What is this project about?"></textarea>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-outline" @click="close">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="isLoading">
            {{ isLoading ? 'Saving…' : isEditing ? 'Save Changes' : 'Create Project' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProjectModal',
  props: { project: { type: Object, default: null } },
  data() {
    return { form: { name: '', description: '' }, isLoading: false, errors: [] }
  },
  computed: { isEditing() { return !!this.project } },
  watch: {
    project: {
      immediate: true,
      handler(v) { if (v) this.form = { name: v.name, description: v.description || '' } }
    }
  },
  methods: {
    close() { this.$emit('close') },
    async handleSubmit() {
      this.errors = []
      if (!this.form.name.trim()) { this.errors.push('Project name is required'); return }
      this.isLoading = true
      try {
        if (this.isEditing) {
          await this.$store.dispatch('projects/updateProject', {
            projectId: this.project.id, name: this.form.name, description: this.form.description
          })
          this.$emit('updated')
        } else {
          await this.$store.dispatch('projects/createProject', {
            name: this.form.name, description: this.form.description
          })
          this.$emit('created')
        }
        this.close()
      } catch (e) {
        this.errors.push(e.response?.data?.message || e.message || 'Operation failed')
      } finally { this.isLoading = false }
    }
  }
}
</script>

<style scoped>
/* Inherits global modal styles from clay-theme.css */
</style>
