import Vue from 'vue'
import Vuex from 'vuex'

import authent from './modules/authent'
import events from './modules/events'
import snackbar from './modules/snackbar'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    authent,
    events,
    snackbar
  }
})
