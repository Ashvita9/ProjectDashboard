<template>
  <transition-group name="notification" tag="div" class="toast-container">
    <div v-for="notification in notifications" :key="notification.id" :class="['toast', `toast-${notification.type}`]">
      <span class="toast-dot" :class="`dot-${notification.type}`"></span>
      <span class="toast-msg">{{ notification.message }}</span>
      <button class="toast-close" @click="removeNotification(notification.id)">×</button>
    </div>
  </transition-group>
</template>

<script>
import { eventBus } from '@/bus/eventBus'

let notificationId = 0

export default {
  name: 'NotificationCenter',
  data() {
    return {
      notifications: [],
      notifyHandler: null
    }
  },
  mounted() {
    this.notifyHandler = (notification) => {
      const id = notificationId++
      this.notifications.push({ id, ...notification })
      setTimeout(() => this.removeNotification(id), 4000)
    }
    eventBus.onNotify(this.notifyHandler)
  },
  beforeDestroy() {
    if (this.notifyHandler) {
      eventBus.$off('notify', this.notifyHandler)
    }
  },
  methods: {
    removeNotification(id) {
      const i = this.notifications.findIndex(n => n.id === id)
      if (i !== -1) this.notifications.splice(i, 1)
    }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 380px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-lg);
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
  animation: slideIn 0.25s var(--ease);
}

.toast-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot-success {
  background: var(--color-success);
}

.dot-error {
  background: var(--color-danger);
}

.dot-info {
  background: var(--color-info);
}

.dot-warning {
  background: var(--color-warning);
}

.toast-msg {
  flex: 1;
}

.toast-close {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 18px;
  cursor: pointer;
  padding: 0 4px;
  box-shadow: none;
  transition: color 0.15s var(--ease);
}

.toast-close:hover {
  color: var(--text-primary);
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }

  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification-leave-active {
  animation: slideOut 0.2s var(--ease);
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }

  to {
    transform: translateX(100%);
    opacity: 0;
  }
}
</style>
