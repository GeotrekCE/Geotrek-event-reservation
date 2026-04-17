import { createApp } from "vue";

import PrimeVue from "primevue/config";
import ConfirmationService from "primevue/confirmationservice";
import ToastService from "primevue/toastservice";
import Aura from "@primeuix/themes/aura";
import "./style.css";

import App from "./App.vue";

import { useAuthStore } from "./stores/auth";

// import './plugins/yup'
import router from "./router";
import { createPinia } from "pinia";

export const pinia = createPinia();
/**
 * Check the auth
 */
async function boot() {
  /**
   * First, check the auth of user before creating Vue App
   */
  const authStore = useAuthStore(pinia);
  await authStore.checkAuth();

  /**
   * Now, we know if user is auth or not,
   * render the app
   */
  const app = createApp(App);

  app.use(PrimeVue, {
    theme: {
      preset: Aura,
    },
  });
  app.use(ConfirmationService);
  app.use(ToastService);
  app.use(pinia);
  app.use(router);

  app.mount("#app");
}

boot();

// const app = createApp(App);
// app.use(PrimeVue, {
//     theme: {
//         preset: Aura
//     }
// });

// app.use(PrimeVue);
// app.mount('#app');
