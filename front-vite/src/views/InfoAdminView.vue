<template>
  <header class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900">
        Informations à destination des administateurs
      </h1>
    </div>
  </header>
  <main class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 px-4 py-6">
    <section>
      <div v-if="loading">Loading...</div>
      <div v-html="markdownToHTML" v-else></div>

    </section>
  </main>

</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { marked } from 'marked';
import { useAuthStore } from '@/stores/auth'

const markdownToHTML = ref('')
const loading = ref(false)

const authStore = useAuthStore()

onMounted(async () => {
  loading.value = true
  const response = await fetch('page_info_admin.md')
  const text = await response.text()
  markdownToHTML.value = marked(text) || 'Erreur lors de la récupération des informations à afficher.'
  loading.value = false
})
</script>
