<template>
  <header class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900">
        Bienvenue !
      </h1>
    </div>
  </header>
  <main class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 px-4 py-6">
    <section class="pb-12 mx-auto">
    	<p class="mb-8">
        Bienvenue sur l'outil de gestion des réservations d'événement du {{ parkLabel }}.
    	</p>

      <p class="flex items-center">
        <router-link
          v-if="!authStore.isAuth"
          to="/login"
          class="rounded-sm bg-sky-600 px-3 py-1.5 text-sm font-medium leading-6 text-white shadow-sm hover:bg-sky-500 my-4 mx-auto"
        >
          Aller à la page de connexion
        </router-link>
      </p>

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

const parkLabel = CONFIGURATION.PARK_LABEL

const authStore = useAuthStore()

onMounted(async() => {
  loading.value = true
  const response = await fetch('page_accueil.md')
  const text = await response.text()
  markdownToHTML.value = marked(text) || 'Erreur lors de la récupération des informations à afficher.'
  loading.value = false
})
</script>
