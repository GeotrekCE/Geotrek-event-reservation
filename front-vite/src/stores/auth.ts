import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { postApiData } from '@/utils/api'

interface User {
  email: string
  is_admin: boolean
}

export const useAuthStore = defineStore('auth', () => {

  const user = ref<null | User>(null)

  const isAuth = computed(() => {
    return !!user.value
  })

  const isAdmin = computed(() => {
    return user.value?.is_admin
  })

  /**
   * Call the API to log the user,
   * retrieve user data
   * and store it in the auth state
   */
  async function login (token: string) {
    user.value = await postApiData(
      CONFIGURATION.URL_APPLICATION, 
      'login', 
      { login_token: token }, 
      false
    )
  }

  function logout () {
    user.value = null
  }

  async function sendLoginEmail (email: string) {
    await postApiData(CONFIGURATION.URL_APPLICATION, 'send-login-email', { email }, false)
  }

  return { user, login, logout, sendLoginEmail, isAuth, isAdmin }
})