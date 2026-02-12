<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title">{{ isEditing ? 'Edit Project' : 'Create New Project' }}</h2>
      </div>

      <div v-if="errors.length" class="alert alert-error mb-20">
        <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="name">Project Name</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            placeholder="Enter project name"
          />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea
            id="description"
            v-model="form.description"
            placeholder="Enter project description"
          ></textarea>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-outline" @click="close">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="isLoading">
            {{ isLoading ? 'Saving...' : 'Save Project' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProjectModal',
  props: {
    project: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      form: {
        name: '',
        description: ''
      },
      isLoading: false,
      errors: []
    }
  },
  computed: {
    isEditing() {
      return !!this.project
    }
  },
  watch: {
    project: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.form = {
            name: newVal.name,
            description: newVal.description || ''
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

      if (!this.form.name.trim()) {
        this.errors.push('Project name is required')
        return
      }

      this.isLoading = true

      try {
        if (this.isEditing) {
          await this.$store.dispatch('projects/updateProject', {
            projectId: this.project.id,
            name: this.form.name,
            description: this.form.description
          })
          this.$emit('updated')
        } else {
          await this.$store.dispatch('projects/createProject', {
            name: this.form.name,
            description: this.form.description
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
