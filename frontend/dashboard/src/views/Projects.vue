<template>
  <div class="projects-page">
    <div class="page-header">
      <h1>My Projects</h1>
      <button class="btn btn-primary" @click="showCreateModal = true">
        + Create New Project
      </button>
    </div>

    <div v-if="errors.length" class="alert alert-error">
      <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
    </div>

    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
    </div>

    <div v-else-if="projects.length > 0" class="projects-grid">
      <ProjectCard
        v-for="project in projects"
        :key="project.id"
        :project="project"
        @edit="editProject(project)"
        @deleted="handleProjectDeleted"
      />
    </div>

    <div v-else class="empty-state">
      <h2>No Projects Yet</h2>
      <p>Create your first project to get started!</p>
      <button class="btn btn-primary" @click="showCreateModal = true">
        Create Your First Project
      </button>
    </div>

    <ProjectModal
      v-if="showCreateModal || showEditModal"
      :project="editingProject"
      @close="closeModal"
      @created="handleProjectCreated"
      @updated="handleProjectUpdated"
    />
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import ProjectCard from '@/components/Project/ProjectCard.vue'
import ProjectModal from '@/components/Project/ProjectModal.vue'

export default {
  name: 'Projects',
  components: {
    ProjectCard,
    ProjectModal
  },
  data() {
    return {
      showCreateModal: false,
      showEditModal: false,
      editingProject: null,
      errors: []
    }
  },
  computed: {
    ...mapState('projects', ['isLoading']),
    ...mapGetters('projects', ['allProjects']),
    projects() {
      return this.allProjects
    }
  },
  mounted() {
    this.loadProjects()
  },
  methods: {
    async loadProjects() {
      try {
        const userId = this.$store.state.auth.userId
        await this.$store.dispatch('projects/fetchProjects', userId)
      } catch (error) {
        const errorMsg = error.response?.data?.message || 'Failed to load projects'
        this.errors.push(errorMsg)
      }
    },
    editProject(project) {
      this.editingProject = project
      this.showEditModal = true
    },
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.editingProject = null
    },
    handleProjectCreated() {
      this.closeModal()
      this.errors = []
    },
    handleProjectUpdated() {
      this.closeModal()
      this.errors = []
    },
    handleProjectDeleted() {
      this.errors = []
    }
  }
}
</script>

<style scoped>
.projects-page {
  padding: 30px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h1 {
  color: var(--clay-primary);
  margin: 0;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-state h2 {
  color: var(--clay-primary);
  margin-bottom: 10px;
}

.empty-state p {
  color: var(--clay-accent-info);
  margin-bottom: 20px;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: 60px;
}

@media (max-width: 768px) {
  .projects-page {
    padding: 20px;
  }

  .page-header {
    flex-direction: column;
    gap: 15px;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
