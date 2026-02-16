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

        <div class="form-group">
          <label for="start_date">Start Date</label>
          <flat-pickr v-model="form.start_date" :config="dateConfig" />
        </div>

        <div class="form-group">
          <label for="deployment_date">Deployment Date</label>
          <flat-pickr v-model="form.deployment_date" :config="dateConfig" />
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
import FlatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'

export default {
  name: 'ProjectModal',
  components: { FlatPickr },
  props: { project: { type: Object, default: null } },
  data() {
    return {
      form: { name: '', description: '', start_date: '', deployment_date: '' },
      dateConfig: { dateFormat: 'Y-m-d', allowInput: true },
      isLoading: false,
      errors: []
    }
  },
  computed: { isEditing() { return !!this.project } },
  watch: {
    project: {
      immediate: true,
      handler(v) {
        if (v) {
          // normalize incoming dates to YYYY-MM-DD for input[type=date]
          const fmt = d => {
            try { return d ? new Date(d).toISOString().slice(0, 10) : '' } catch (e) { return '' }
          }
          this.form = {
            name: v.name,
            description: v.description || '',
            start_date: fmt(v.start_date),
            deployment_date: fmt(v.deployment_date)
          }
        }
      }
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
            projectId: this.project.id,
            name: this.form.name,
            description: this.form.description,
            start_date: this.form.start_date || null,
            deployment_date: this.form.deployment_date || null
          })
          this.$emit('updated')
        } else {
          await this.$store.dispatch('projects/createProject', {
            name: this.form.name,
            description: this.form.description,
            start_date: this.form.start_date || null,
            deployment_date: this.form.deployment_date || null
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
