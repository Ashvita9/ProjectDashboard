import Vue from 'vue'

export const eventBus = new Vue({
  methods: {
    notifySuccess(message) {
      this.$emit('notify', {
        type: 'success',
        message
      })
    },
    notifyError(message) {
      this.$emit('notify', {
        type: 'error',
        message
      })
    },
    notifyInfo(message) {
      this.$emit('notify', {
        type: 'info',
        message
      })
    },
    notifyWarning(message) {
      this.$emit('notify', {
        type: 'warning',
        message
      })
    },
    onNotify(callback) {
      this.$on('notify', callback)
    }
  }
})
