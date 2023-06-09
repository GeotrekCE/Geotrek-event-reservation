import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { postApiData } from '@/utils/api'
import router from '@/router'

interface User {
  id: number
  id_role: number
}

export const useAuthStore = defineStore('auth', () => {

  const user = ref<null | User>(null)
  const redirectOnLogin = ref('')

  const isAuth = computed(() => {
      if (!user.value) {
        return false;
      }
      return !!(user.value && user.value.id_role);
  })

  /**
   * Call the API to log the user,
   * retrieve user data
   * and store it in the auth state
   */
  async function login (username: string, password: string) {
    const userData = {
      login: username,
      password,
    };

    const response = await (postApiData(CONFIGURATION.URL_APPLICATION, 'auth/login', userData, false) as Promise<{ user: any, expires: any }>);
    user.value = { ...response.user, expires: response.expires };

    if (redirectOnLogin.value !== undefined) {
      router.push({ path: redirectOnLogin.value });
    } else {
      router.push({ path: '/' });
    }

  }

  function logout () {
    user.value = null
  }

  return { user, login, logout, redirectOnLogin, isAuth }
})