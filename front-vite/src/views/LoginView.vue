<template>
  <div class="flex flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Recevoir mon lien de connexion</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm md:max-w-md">
      <form class="space-y-6" @submit.prevent="login">
        <div>
          <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Adresse email</label>
          <div class="mt-2">
            <input
              id="email"
              name="email"
              type="email"
              autocomplete="email"
              required
              v-model="email"
              class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="flex w-full justify-center rounded-sm bg-sky-600 px-3 py-1.5 text-sm font-medium leading-6 text-white shadow-sm hover:bg-sky-500 disabled:bg-sky-200"
            :disabled="loading"
          >
            Recevoir mon lien de connexion
          </button>
        </div>
        <div v-if="success">
          Un email de connexion vient de vous être envoyé.<br/>
          En cliquant sur le lien contenu dans ce dernier, vous pourrez vous connecter.
        </div>
        <div v-if="error" class="text-red-500">
          Une erreur est survenue pendant la demande de votre lien de connexion.<br/>
          Merci d'essayer à nouveau.<br/>
          Si vous n'arrivez pas à obtenir le lien de connexion, merci de prendre contact avec le parc.        
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRoute } from 'vue-router';

const loading = ref(false)
const success = ref(false)
const error = ref(false)

const route = useRoute()
const email = ref(route.query.email as string)

const authStore = useAuthStore()
async function login() {
  if (!email.value) return
  loading.value = true
  error.value = false
  try {
    await authStore.sendLoginEmail(email.value)
    success.value = true
  } catch {
    error.value = true
  }
  loading.value = false
}

</script>
