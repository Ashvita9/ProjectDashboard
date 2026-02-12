<template>
  <transition-group
    name="notification"
    tag="div"
    class="notifications-container"
  >
    <div
      v-for="notification in notifications"
      :key="notification.id"
      :class="['notification-item', `notification-${notification.type}`]"
    >
      {{ notification.message }}
      <button class="close-btn" @click="removeNotification(notification.id)">×</button>
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
      notifications: []
    }
  },
  mounted() {
    eventBus.onNotify((notification) => {
      const id = notificationId++
      const item = {
        id,
        ...notification
      }
      this.notifications.push(item)

      // Auto-remove after 4 seconds
      setTimeout(() => {
        this.removeNotification(id)
      }, 4000)
    })
  },
  methods: {
    removeNotification(id) {
      const index = this.notifications.findIndex(n => n.id === id)
      if (index !== -1) {
        this.notifications.splice(index, 1)
      }
    }
  }
}
</script>

<style scoped>
.notifications-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  max-width: 400px;
}

.notification-item {
  background-color: white;
  padding: 15px 20px;
  border-radius: 6px;
  margin-bottom: 10px;
  box-shadow: 0 4px 12px rgba(42, 36, 33, 0.2);
  border-left: 4px solid;
  display: flex;
  justify-content: space-between;
  align-items: center;
  animation: slideIn 0.3s ease;
}

.notification-success {
  border-left-color: var(--clay-accent-success);
  background-color: #F0F8F0;
  color: #4A5C2A;
}

.notification-error {
  border-left-color: var(--clay-accent-danger);
  background-color: #F8F0F0;
  color: #5C4A4A;
}

.notification-info {
  border-left-color: var(--clay-accent-info);
  background-color: #F5F3F0;
  color: var(--clay-primary);
}

.notification-warning {
  border-left-color: var(--clay-accent-warning);
  background-color: #FFF5EE;
  color: #8B6A4A;
}

.close-btn {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 20px;
  padding: 0;
  margin-left: 10px;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.close-btn:hover {
  opacity: 1;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification-leave-active {
  animation: slideOut 0.3s ease;
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(400px);
    opacity: 0;
  }
}
</style>
