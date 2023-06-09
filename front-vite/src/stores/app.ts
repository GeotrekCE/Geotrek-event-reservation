import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {
  const snackbarInfo = ref({
    message: undefined,
    color: 'success',
    show: false
  })

  return { snackbarInfo }
})