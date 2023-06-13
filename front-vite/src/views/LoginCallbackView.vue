<template>
  <header class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900">
        Connexion...
      </h1>
    </div>
  </header>
  <main class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 px-4 py-6">
    <section class="pb-12">
    	<div v-if="loading">
    		Vérification de votre authentification...
    	</div>
    	<template v-else>
    		<div v-if="success">Connexion OK. Redirection...</div>
    		<div v-if="error">Connexion NOK</div>
    	</template>
    </section>
  </main>

</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth';
import { ref, onMounted } from 'vue'
import { ROUTES_PATHS } from '@/router'

const token = useRoute().query.token as string
const authStore = useAuthStore()
const router = useRouter()

const loading = ref(false)
const success = ref(false)
const error = ref(false)

onMounted(async () => {
	loading.value = true
	error.value = false
	success.value = false
	try {
		await authStore.login(token)
		success.value = true
		/**
		 * Si l'utilisateur est admin, on le renvoie sur la page des événements
		 */
		if (authStore.isAdmin) {
			router.push(ROUTES_PATHS.EVENT_LISTING)
		} else {
  		/**
  		 * Sinon, sur les réservations
  		 */
			router.push(ROUTES_PATHS.RESA_LISTING)
		}
	} catch {
		error.value = true
	}
	loading.value = false
})

</script>