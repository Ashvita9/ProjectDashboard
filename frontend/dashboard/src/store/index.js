import Vue from 'vue'
import Vuex from 'vuex'
import auth from './authModule'
import projects from './projectsModule'
import tasks from './tasksModule'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    auth,
    projects,
    tasks
  }
})
