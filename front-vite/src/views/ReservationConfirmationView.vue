<template>

  <header class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900">
        Confirmation de la réservation de l'événement {{ name }}
      </h1>
    </div>
  </header>


  <main
    class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 px-4 py-6"
  >
    <div v-if="loading" class="space-y-6">
      <p>Confirmation en cours...</p>
      <p>Merci de patienter...</p>
    </div>
    <div v-else-if="success" class="space-y-6">
      <h2 class="text-xl font-medium leading-7 text-gray-900 mt-10 mb-4">
        Merci !
      </h2>
      <p>
        Nous avons bien enregistré la confirmation de votre réservation.
      </p>
      <p>
        Votre réservation a été <strong>acceptée</strong>, vous allez recevoir un email précisant cela... (texte à modifier)
      </p>
      <p>
        Votre réservation a été mise en <strong>liste d'attente</strong>, il n'y a plus assez de place pour cet événement.
      </p>
      <p>
        Dans le cas où des places venaient à se libérer, vous serez informé par email ou contacté par le parc directement.
      </p>
    </div>
    <div v-else class="space-y-6">
      <p>
        Nous sommes désolé, votre confirmation n'a pas pu aboutir.
      </p>
      <p>
        Une erreur est survenue lors de la confirmation de votre réservation.
      </p>
      <p>
        Vous pouvez essayer de recharger cette page pour tenter une nouvelle confirmation,
        ou vous pouvez prendre contact avec le parc pour confirmer manuellement votre réservation.

        (mettre les coordonnées du parc)
      </p>
      <p>
        Pour information, erreur rencontrée :
      </p>
      <p class="text-red-500">
        {{ error }}
      </p>
    </div>
  </main>

</template>

<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import { useRoute } from 'vue-router'
import { confirmReservation } from '@/utils/appli_api'

const currentRoute = useRoute()
const token = currentRoute.query.token as string
const name = currentRoute.query.name

const loading = ref(false)
const success = ref(false)
const error = ref<any>(null)

onBeforeMount(async () => {
  loading.value = true
  try {
    await confirmReservation({resa_token: token})
    success.value = true
  } catch(e) {
    console.error(e)
    error.value = e
  }
  loading.value = false
})

</script>