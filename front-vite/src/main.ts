import { createApp } from 'vue'

import { pinia } from './plugins/pinia'
import './plugins/yup'
import router from './router'

/**
 * Prime Vue
 */
import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/lara-light-teal/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

import './index.css'


import App from './App.vue'

const app = createApp(App)

app.use(PrimeVue)

app.use(pinia)
app.use(router)

app.mount('#app')
