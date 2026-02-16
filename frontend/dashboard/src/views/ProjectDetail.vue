<template>
  <div class="page">
    <!-- Loading overlay for drag operations -->
    <transition name="fade">
      <div v-if="isMoving" class="moving-overlay">
        <div class="moving-spinner"></div>
        <span>Updating...</span>
      </div>
    </transition>

    <div v-if="isLoading" class="center-state">
      <div class="spinner"></div>
      <p class="loading-text">Loading project...</p>
    </div>

    <template v-else-if="activeProject">
      <!-- Header -->
      <div class="detail-header fade-in">
        <div class="header-left">
          <router-link to="/projects" class="back-link">← Projects</router-link>
          <h1>{{ activeProject.name }}</h1>
          <p v-if="activeProject.description" class="detail-desc">{{ activeProject.description }}</p>
        </div>
        <div class="header-actions">
          <button class="btn btn-outline" @click="editProject">Edit</button>
          <button class="btn btn-primary" @click="showCreateTaskModal = true">+ Add Task</button>
        </div>
      </div>

      <div v-if="errors.length" class="alert alert-error">
        <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
      </div>

      <!-- Kanban Board -->
      <div class="board">
        <div class="board-col slide-up" v-for="(col, colIndex) in columns" :key="col.key" :style="{ animationDelay: `${colIndex * 0.1}s` }">
          <div class="col-header">
            <span class="col-dot" :class="`dot-${col.key}`"></span>
            <span class="col-title">{{ col.label }}</span>
            <span class="col-count">{{ columnLists[col.key].length }}</span>
          </div>
          <div class="col-body" :class="{ 'col-drop-target': activeDropTarget === col.key }">
            <!-- Loading skeleton -->
            <div v-if="isLoadingTasks" class="skeleton-list">
              <div class="skeleton-card" v-for="n in 2" :key="n"></div>
            </div>
            <draggable
              v-else
              :list="columnLists[col.key]"
              group="tasks"
              :animation="200"
              ghost-class="drag-ghost"
              chosen-class="drag-chosen"
              drag-class="drag-active"
              :empty-insert-threshold="100"
              @start="onDragStart(col.key)"
              @end="onDragEnd"
              @change="onDragChange(col.key, $event)"
              class="task-list"
            >
              <div v-for="(task, index) in columnLists[col.key]" :key="task.id" class="drag-item" :style="{ animationDelay: `${index * 0.05}s` }">
                <TaskCard
                  :task="task"
                  @edit="editTask(task)"
                  @deleted="loadProjectTasks"
                />
              </div>
            </draggable>
            <div v-if="!isLoadingTasks && columnLists[col.key].length === 0 && !isDragging" class="col-empty-text">No tasks</div>
          </div>
        </div>
      </div>

      <div v-if="tasksByProjectId.length === 0 && !isLoading" class="empty-board">
        <p>No tasks yet. Click <strong>+ Add Task</strong> to start.</p>
      </div>

      <ProjectModal v-if="showEditProjectModal" :project="activeProject" @close="showEditProjectModal = false"
        @updated="handleProjectUpdated" />

      <TaskModal v-if="showCreateTaskModal || showEditTaskModal" :task="editingTask" @close="closeTaskModal"
        @created="handleTaskCreated" @updated="handleTaskUpdated" />
    </template>

    <div v-else class="center-state">
      <p>Project not found.</p>
      <router-link to="/projects" class="btn btn-primary">Back to Projects</router-link>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import TaskCard from '@/components/Task/TaskCard.vue'
import { taskService } from '@/services/task'
import draggable from 'vuedraggable'
import { eventBus } from '@/bus/eventBus'
import TaskModal from '@/components/Task/TaskModal.vue'
import ProjectModal from '@/components/Project/ProjectModal.vue'

export default {
  name: 'ProjectDetail',
  components: { TaskCard, TaskModal, ProjectModal, draggable },
  data() {
    return {
      isLoading: false,
      isLoadingTasks: false,
      isMoving: false,
      isDragging: false,
      dragFromCol: null,
      errors: [],
      showCreateTaskModal: false,
      showEditTaskModal: false,
      showEditProjectModal: false,
      editingTask: null,
      activeDropTarget: null,
      columnLists: {
        todo: [],
        in_progress: [],
        done: []
      }
    }
  },
  computed: {
    ...mapState('projects', ['activeProject']),
    projectId() { return this.$route.params.id },
    tasksByProjectId() {
      return this.$store.state.tasks.tasksByProject[this.projectId] || []
    },
    columns() {
      return [
        { key: 'todo', label: 'To Do', tasks: this.tasksByProjectId.filter(t => t.status === 'todo') },
        { key: 'in_progress', label: 'In Progress', tasks: this.tasksByProjectId.filter(t => t.status === 'in_progress') },
        { key: 'done', label: 'Done', tasks: this.tasksByProjectId.filter(t => t.status === 'done') }
      ]
    }
  },
  watch: {
    '$route.params.id': { immediate: true, handler(id) { this.loadProjectData(id) } }
  },
  methods: {
    async loadProjectData(projectId) {
      this.isLoading = true; this.errors = []
      try {
        const userId = this.$store.state.auth.userId
        if (this.$store.getters['projects/projectCount'] === 0) {
          await this.$store.dispatch('projects/fetchProjects', userId)
        }
        const project = this.$store.getters['projects/getProjectById'](projectId)
        if (project) this.$store.dispatch('projects/setActiveProject', project)
        await this.loadProjectTasks()
      } catch (e) { this.errors.push(e.response?.data?.message || 'Failed to load project') }
      finally { this.isLoading = false }
    },
    async loadProjectTasks() {
      this.isLoadingTasks = true
      try {
        await this.$store.dispatch('tasks/fetchTasksByProject', this.projectId)
        const tasks = this.tasksByProjectId || []
        // populate mutable lists used by draggable
        const todo = tasks.filter(t => t.status === 'todo')
        const inProgress = tasks.filter(t => t.status === 'in_progress')
        const done = tasks.filter(t => t.status === 'done')
        this.columnLists.todo.splice(0, this.columnLists.todo.length, ...todo)
        this.columnLists.in_progress.splice(0, this.columnLists.in_progress.length, ...inProgress)
        this.columnLists.done.splice(0, this.columnLists.done.length, ...done)
      } catch (e) { this.errors.push(e.response?.data?.message || 'Failed to load tasks') }
      finally { this.isLoadingTasks = false }
    },
    editProject() { this.showEditProjectModal = true },
    editTask(task) { this.editingTask = task; this.showEditTaskModal = true },
    closeTaskModal() { this.showCreateTaskModal = false; this.showEditTaskModal = false; this.editingTask = null },
    handleProjectUpdated() { this.showEditProjectModal = false },
    handleTaskCreated() { this.closeTaskModal(); this.loadProjectTasks() },
    handleTaskUpdated() { this.closeTaskModal(); this.loadProjectTasks() },
    onDragStart(fromCol) {
      this.isDragging = true
      this.dragFromCol = fromCol
    },
    onDragEnd() {
      this.isDragging = false
      this.dragFromCol = null
    },
    async onDragChange(colKey, evt) {
      // evt has properties: added, removed, moved. For cross-list move, added will be present.
      try {
        if (evt.added) {
          // element has already been inserted into columnLists[colKey] by draggable
          const task = evt.added.element
          if (!task) return
          const taskId = task.id
          if (task.status === colKey) return

          // optimistic: update the task object in-place
          const old = { ...task }
          task.status = colKey
          this.$store.commit('tasks/UPDATE_TASK', task)
          this.isMoving = true

          try {
            await this.updateTaskStatus(taskId, colKey)
            eventBus.notifySuccess('Task moved')
          } catch (err) {
            // rollback: restore old status and refresh
            task.status = old.status
            this.$store.commit('tasks/UPDATE_TASK', task)
            eventBus.notifyError(err.response?.data?.message || 'Failed to move task')
            await this.loadProjectTasks()
          } finally {
            this.isMoving = false
          }
        }
      } finally {
        this.activeDropTarget = null
      }
    },
    async updateTaskStatus(taskId, status) {
      const userId = this.$store.state.auth.userId
      const resp = await taskService.partialUpdateTask(taskId, { status, user_id: userId })
      const updated = resp.data?.task || resp.data
      if (updated) {
        // commit update to store for immediate UI sync
        this.$store.commit('tasks/UPDATE_TASK', updated)
      }
      return updated
    }
  }
}
</script>

<style scoped>
.page {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 24px;
}

/* Header */
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
  gap: 20px;
}

.header-left {
  flex: 1;
}

.back-link {
  font-size: 13px;
  color: var(--text-muted);
  display: inline-block;
  margin-bottom: 12px;
  transition: color 0.15s var(--ease);
}

.back-link:hover {
  color: var(--accent-light);
}

.detail-header h1 {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-bottom: 6px;
}

.detail-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.header-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
  margin-top: 28px;
}

/* Kanban Board */
.board {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 8px;
}

.board-col {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  min-height: 300px;
}

.col-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 18px;
  border-bottom: 1px solid var(--border);
}

.col-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot-todo {
  background: var(--text-muted);
}

.dot-in_progress {
  background: var(--color-warning);
}

.dot-done {
  background: var(--color-success);
}

.col-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.col-count {
  margin-left: auto;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
  background: var(--bg-hover);
  padding: 2px 8px;
  border-radius: var(--radius-full);
}

.col-body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  flex: 1;
  position: relative;
}

.col-drop-target {
  box-shadow: inset 0 0 0 3px rgba(124, 58, 237, 0.12);
  transform: translateZ(0);
}

.col-empty-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 13px;
  color: var(--text-muted);
  pointer-events: none;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
  min-height: 150px;
  padding: 4px;
  border-radius: var(--radius-sm);
  transition: background 0.15s ease;
}

.task-list:empty,
.task-list:not(:has(.drag-item)) {
  background: rgba(124, 58, 237, 0.03);
  border: 2px dashed rgba(124, 58, 237, 0.15);
}

.drag-item {
  cursor: grab;
  transition: transform 0.15s var(--ease), opacity 0.15s var(--ease);
}

.drag-item:active {
  cursor: grabbing;
}

.drag-ghost {
  opacity: 0.5 !important;
}

.drag-chosen {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.empty-board {
  text-align: center;
  padding: 40px;
  color: var(--text-muted);
  font-size: 14px;
  margin-top: 20px;
}

.center-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px;
  gap: 16px;
  color: var(--text-muted);
}

.loading-text {
  font-size: 14px;
  color: var(--text-muted);
  animation: pulse 1.5s ease-in-out infinite;
}

/* Moving overlay */
.moving-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  z-index: 1000;
  color: white;
  font-size: 14px;
  font-weight: 500;
  backdrop-filter: blur(2px);
}

.moving-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Skeleton loading */
.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton-card {
  height: 80px;
  background: linear-gradient(90deg, var(--bg-hover) 25%, var(--bg-elevated) 50%, var(--bg-hover) 75%);
  background-size: 200% 100%;
  border-radius: var(--radius-sm);
  animation: shimmer 1.5s infinite;
}

/* Animations */
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}

.slide-up {
  animation: slideUp 0.4s ease-out forwards;
  opacity: 0;
}

/* Transition group animations */
.task-list-enter-active {
  animation: slideUp 0.3s ease-out;
}

.task-list-leave-active {
  animation: fadeIn 0.2s ease-out reverse;
}

.task-list-move {
  transition: transform 0.3s ease;
}

.task-transition-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Drag states */
.drag-active {
  z-index: 100;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .board {
    grid-template-columns: 1fr;
  }

  .detail-header {
    flex-direction: column;
  }

  .header-actions {
    margin-top: 16px;
  }
}
</style>
