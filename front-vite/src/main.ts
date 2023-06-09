import { createApp } from 'vue'

// import { vuetify } from './plugins/vuetify'
import { pinia } from './plugins/pinia'
import router from './router'

import './index.css'

/**
 * Prime Vue
 */
import PrimeVue from 'primevue/config'
// import 'primevue/resources/themes/lara-light-teal/theme.css'
// import 'primevue/resources/primevue.min.css'
// import 'primeicons/primeicons.css'   

import App from './App.vue'

const app = createApp(App)

app.use(PrimeVue)

// app.use(vuetify)
app.use(pinia)
app.use(router)

app.mount('#app')
