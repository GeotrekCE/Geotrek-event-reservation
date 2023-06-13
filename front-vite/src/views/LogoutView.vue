<template>
  <header class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900">
        Déconnexion...
      </h1>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth';
import { onBeforeMount } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

onBeforeMount(async () => {
  authStore.logout()
  router.push('/')
})

</script>