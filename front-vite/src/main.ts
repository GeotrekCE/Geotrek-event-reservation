import { createApp } from 'vue'

import { pinia } from './plugins/pinia'
import './plugins/yup'
import router from './router'

/**
 * Prime Vue
 */
import PrimeVue from 'primevue/config'
import ConfirmationService from 'primevue/confirmationservice'
import 'primevue/resources/themes/lara-light-teal/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

import './index.css'

import { useAuthStore } from './stores/auth'


import App from './App.vue'

/**
 * Check the auth
 */
async function boot() {
  /**
   * First, check the auth of user before creating Vue App
   */
  const authStore = useAuthStore(pinia)
  await authStore.checkAuth()

  /**
   * Now, we know if user is auth or not,
   * render the app
   */
  const app = createApp(App)

  app.use(PrimeVue)
  app.use(ConfirmationService)

  app.use(pinia)
  app.use(router)

  app.mount('#app')
}

boot()
