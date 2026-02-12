<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h1>Projects</h1>
        <p class="page-sub">Manage and organize your work.</p>
      </div>
      <button class="btn btn-primary" @click="showCreateModal = true">+ New Project</button>
    </div>

    <div v-if="errors.length" class="alert alert-error">
      <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
    </div>

    <div v-if="isLoading" class="center-state">
      <div class="spinner"></div>
    </div>

    <div v-else-if="projects.length > 0" class="project-grid">
      <ProjectCard v-for="project in projects" :key="project.id" :project="project" @edit="editProject(project)"
        @deleted="handleProjectDeleted" />
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">◇</div>
      <h3>No projects yet</h3>
      <p>Create your first project to get started.</p>
      <button class="btn btn-primary" @click="showCreateModal = true">Create Project</button>
    </div>

    <ProjectModal v-if="showCreateModal || showEditModal" :project="editingProject" @close="closeModal"
      @created="handleProjectCreated" @updated="handleProjectUpdated" />
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import ProjectCard from '@/components/Project/ProjectCard.vue'
import ProjectModal from '@/components/Project/ProjectModal.vue'

export default {
  name: 'Projects',
  components: { ProjectCard, ProjectModal },
  data() {
    return { showCreateModal: false, showEditModal: false, editingProject: null, errors: [] }
  },
  computed: {
    ...mapState('projects', ['isLoading']),
    ...mapGetters('projects', ['allProjects']),
    projects() { return this.allProjects }
  },
  mounted() { this.loadProjects() },
  methods: {
    async loadProjects() {
      try {
        await this.$store.dispatch('projects/fetchProjects', this.$store.state.auth.userId)
      } catch (e) { this.errors.push(e.response?.data?.message || 'Failed to load projects') }
    },
    editProject(project) { this.editingProject = project; this.showEditModal = true },
    closeModal() { this.showCreateModal = false; this.showEditModal = false; this.editingProject = null },
    handleProjectCreated() { this.closeModal(); this.errors = [] },
    handleProjectUpdated() { this.closeModal(); this.errors = [] },
    handleProjectDeleted() { this.errors = [] }
  }
}
</script>

<style scoped>
.page {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 28px;
  gap: 16px;
}

.page-header h1 {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.page-sub {
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 4px;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 40px;
  color: var(--accent);
  margin-bottom: 16px;
}

.empty-state h3 {
  color: var(--text-primary);
  margin-bottom: 8px;
}

.empty-state p {
  margin-bottom: 20px;
  font-size: 14px;
}

.center-state {
  display: flex;
  justify-content: center;
  padding: 80px;
}

@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .project-grid {
    grid-template-columns: 1fr;
  }
}
</style>
