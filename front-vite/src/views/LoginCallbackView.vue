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
    		<div v-if="error" class="space-y-4">
    			<p>La connexion de l'utilisateur n'a pas pu aboutir...</p>
    			<p>Merci de recommencer la procédure avec l'envoi du mail de connexion.</p>
    			<router-link to="/login" class="text-blue-600 visited:text-purple-600">Aller à la page de connexion</router-link>
    		</div>
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
const redirectTo = useRoute().query.route as string
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
		 * Si le paramètre route est spécifié on le renvoie vers la page demandé sauf si login ou home
		 */
		if (redirectTo && ![ROUTES_PATHS.LOGIN, ROUTES_PATHS.HOME].includes(redirectTo)) {
			router.push(redirectTo)
		}
		else if (authStore.isAdmin) {
			/**
			 * Si l'utilisateur est admin, on le renvoie sur la page des événements
			 */
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