import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { postApiData, getApiData } from '@/utils/api'

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
   * Ask the API to log the user,
   * retrieve user data
   * and store it in the auth state
   */
  async function login (token: string) {
    user.value = await postApiData(
      CONFIGURATION.URL_APPLICATION, 
      'login', 
      { login_token: token },
    )
  }

  /**
   * Ask the API to check if session is still ok
   * To be used at application boot
   */
  async function checkAuth () {
    try {
      user.value = await getApiData(
        CONFIGURATION.URL_APPLICATION, 
        'ping', 
      )
    } catch {
      user.value = null
    }
  }

  /**
   * Ask the API to destroy cookie
   */
  async function logout () {
    user.value = null
    await getApiData(
      CONFIGURATION.URL_APPLICATION,
      'logout',
    )
  }

  /**
   * Ask for sending a password-less email login to the user
   */
  async function sendLoginEmail (email: string) {
    await postApiData(
      CONFIGURATION.URL_APPLICATION,
      'send-login-email',
      { email },
    )
  }

  return {
    user,
    isAuth,
    isAdmin,

    checkAuth,
    login,
    logout,
    sendLoginEmail,
  }
})