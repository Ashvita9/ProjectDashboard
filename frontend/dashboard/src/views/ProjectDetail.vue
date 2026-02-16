<template>
  <div class="page">
    <div v-if="isLoading" class="center-state">
      <div class="spinner"></div>
    </div>

    <template v-else-if="activeProject">
      <!-- Header -->
      <div class="detail-header">
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

      <!-- Debug panel: show runtime lists (temporary) -->
      <div class="debug-panel" style="margin-top:16px; color:var(--text-muted); font-size:13px;">
        <div>tasksByProjectId length: {{ (tasksByProjectId || []).length }}</div>
        <div>columnLists.todo: {{ columnLists.todo.length }} | in_progress: {{ columnLists.in_progress.length }} | done: {{ columnLists.done.length }}</div>
        <pre style="max-height:120px; overflow:auto; background:var(--bg-primary); padding:8px; border-radius:6px;">{{ columnLists }}</pre>
      </div>

      <div v-if="errors.length" class="alert alert-error">
        <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
      </div>

      <!-- Kanban Board -->
      <div class="board">
        <div class="board-col" v-for="col in columns" :key="col.key">
          <div class="col-header">
            <span class="col-dot" :class="`dot-${col.key}`"></span>
            <span class="col-title">{{ col.label }}</span>
            <span class="col-count">{{ col.tasks.length }}</span>
          </div>
          <div class="col-body"
               :class="{ 'col-drop-target': activeDropTarget === col.key }"
               @dragenter.prevent="onDragEnter(col.key)"
               @dragleave.prevent="onDragLeave(col.key)">
            <draggable :list="columnLists[col.key]" :group="{ name: 'tasks', pull: true, put: true }" :animation="180"
                       @change="onDragChange(col.key, $event)" class="task-list" tag="div" item-key="id">
              <template #item="{ element }">
                <div class="task-wrapper">
                  <TaskCard :key="element.id" :task="element" @edit="editTask(element)" @deleted="loadProjectTasks" @status-changed="loadProjectTasks" />
                </div>
              </template>
            </draggable>
            <div v-if="col.tasks.length === 0" class="col-empty">No tasks</div>
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
      isLoading: false, errors: [],
      showCreateTaskModal: false, showEditTaskModal: false,
      showEditProjectModal: false, editingTask: null,
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
      try {
        await this.$store.dispatch('tasks/fetchTasksByProject', this.projectId)
        const tasks = this.tasksByProjectId || []
        // populate mutable lists used by draggable (mutate arrays in-place to preserve references)
        const todo = tasks.filter(t => t.status === 'todo')
        const inProgress = tasks.filter(t => t.status === 'in_progress')
        const done = tasks.filter(t => t.status === 'done')
        this.columnLists.todo.splice(0, this.columnLists.todo.length, ...todo)
        this.columnLists.in_progress.splice(0, this.columnLists.in_progress.length, ...inProgress)
        this.columnLists.done.splice(0, this.columnLists.done.length, ...done)
        console.debug('Loaded tasks', { projectId: this.projectId, total: tasks.length, todo: todo.length, inProgress: inProgress.length, done: done.length })
      } catch (e) { this.errors.push(e.response?.data?.message || 'Failed to load tasks'); console.error(e) }
    },
    editProject() { this.showEditProjectModal = true },
    editTask(task) { this.editingTask = task; this.showEditTaskModal = true },
    closeTaskModal() { this.showCreateTaskModal = false; this.showEditTaskModal = false; this.editingTask = null },
    handleProjectUpdated() { this.showEditProjectModal = false },
    handleTaskCreated() { this.closeTaskModal(); this.loadProjectTasks() },
    handleTaskUpdated() { this.closeTaskModal(); this.loadProjectTasks() },
    onDragEnter(colKey) { this.activeDropTarget = colKey },
    onDragLeave(colKey) { if (this.activeDropTarget === colKey) this.activeDropTarget = null },
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

          try {
            await this.updateTaskStatus(taskId, colKey)
            eventBus.notifySuccess('Task moved')
            // refresh lists to stay in sync with server/state
            await this.loadProjectTasks()
          } catch (err) {
            // rollback: restore old status and refresh
            task.status = old.status
            this.$store.commit('tasks/UPDATE_TASK', task)
            eventBus.notifyError(err.response?.data?.message || 'Failed to move task')
            await this.loadProjectTasks()
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
  gap: 10px;
  flex: 1;
}

.col-drop-target {
  box-shadow: inset 0 0 0 3px rgba(124, 58, 237, 0.12);
  transform: translateZ(0);
}

.col-empty {
  padding: 20px;
  text-align: center;
  font-size: 13px;
  color: var(--text-muted);
}

.task-list .task-card {
  transition: transform 0.18s var(--ease), opacity 0.18s var(--ease);
}

.drag-ghost {
  opacity: 0.9 !important;
  transform: scale(0.98);
}

.task-list > * {
  display: block;
}

.task-wrapper {
  border: 1px dashed rgba(255,255,255,0.04);
  padding: 6px;
  margin-bottom: 8px;
  background: rgba(255,255,255,0.01);
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
