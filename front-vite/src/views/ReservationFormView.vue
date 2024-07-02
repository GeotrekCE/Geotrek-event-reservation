<template>
<div>
  <header class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900">
        Réservation d'un événement
        <template v-if="event">
          ({{ event.name }})
        </template>
      </h1>
    </div>
  </header>

  <main class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 px-4 py-6" v-if="!reservationOpened.value">
    <section class="pb-12 mx-auto space-y-4">
      <p>
        Nous sommes désolés, les réservations ne sont pas possibles.
      </p>
      <p v-if="reservationOpened.text">
        {{ reservationOpened.text }}
      </p>
      <p>
        À très bientôt !
      </p>
    </section>
  </main>

  <main
    class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 px-4 py-6"
    v-else
  >
    <section
      class="border-b border-gray-900/10 pb-12"
      v-if="loadingEvent"
    >

      Chargement en cours... Merci de patienter...

    </section>

    <section
      class="border-b border-gray-900/10 pb-12"
      v-else-if="eventError"
    >

      {{ eventError }}

    </section>

    <template
      v-else-if="status !== STATUS.SUCCESS"
    >
      <section class="border-b border-gray-900/10 pb-12">

        <p>
          Vous vous apprêtez à effectuer une réservation pour l'animation
          <span class="font-medium" v-if="event">{{ event.name }} ({{ formatDateString(event.begin_date) }})</span>
          proposé par le {{ parkLabel }}.
        </p>

        <h2
          class="text-base font-medium leading-7 text-gray-900 mt-10 cursor-pointer"
          @click="isSummaryDisplayed = !isSummaryDisplayed"
        >
          <i
            class="w-4 h-4 pi"
            :class="{
              'pi-chevron-down': isSummaryDisplayed,
              'pi-chevron-right': !isSummaryDisplayed
            }"
          />
          Résumé de l'animation
          {{ isSummaryDisplayed ? '' : '(Cliquez pour afficher)'}}
        </h2>

        <event-summary
          v-if="event && isSummaryDisplayed"
          :event="event"
        />

      </section>

      <section>

        <div class="mt-4">
          <h1 class="text-xl font-medium leading-7 text-gray-900">Inscription</h1>
          <p class="mt-1 text-sm leading-6 text-gray-600">
            En remplissant ce formulaire, puis en le validant,
            vous recevrez un email de confirmation.
            <br/>
            <strong>Veillez bien à confirmer votre inscription via le lien contenu dans cet email.</strong>
          </p>

        </div>

        <event-reservation-form
          class="mt-4"
          @submit="saveReservation"
          :saving="saving"
          :save-error="saveError"
          :original-values="resaToEdit || {}"
        />

      </section>

    </template>

    <template v-else>
      <h2 class="text-xl font-medium leading-7 text-gray-900 mt-10 mb-4">
        Merci pour votre inscription !
      </h2>
      <p class="mb-4">
        Vous allez recevoir un email dans votre boîte de réception
        attestant votre demande de réservation.
      </p>
      <h2 class="text-xl font-medium">
        Mais ce n'est pas fini !
      </h2>
      <p>
        Vous devez <strong>confirmer</strong> cette demande
        en cliquant sur le lien présent dans l'email.
      </p>
    </template>

  </main>
</div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue'
import { useRoute } from 'vue-router'
import { getEvent, postReservation } from '@/utils/appli_api';
import { formatDateString } from '@/utils/formatDate'
import EventSummary from '@/components/EventSummary.vue'
import EventReservationForm from '@/components/EventReservationForm.vue'
import type { ResaEvent } from '@/declaration';
import { isReservationOpened, isReservationGloballyOpened } from '@/utils/isReservationOpened'
import type { Resa } from '@/declaration';
import { useAuthStore } from '@/stores/auth';
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)


const resaToEdit = ref<Resa | null>(null)
const currentRoute = useRoute()
const geotrekId = currentRoute.params.geotrekid

const parkLabel = CONFIGURATION.PARK_LABEL

const STATUS = {
  PRISTINE: 'PRISTINE',
  VALID: 'VALID',
  INVALID: 'INVALID',
  SAVING: 'SAVING',
  ERROR: 'ERROR',
  SUCCESS: 'SUCCESS'
}

/**
 * State local
 */
const isSummaryDisplayed = ref(false)
const status = ref(STATUS.PRISTINE)
const loadingEvent = ref(false)
const eventError = ref('')

/**
 * Chargement de l'événement corrélé
 */
const event = ref<ResaEvent | null>(null)
onBeforeMount(async () => {
  if (!isReservationGloballyOpened()) return
  loadingEvent.value = true
  try {
    event.value = await getEvent(geotrekId)
    if (!event.value.bookable) {
      eventError.value = `L'animation n° ${geotrekId} (${event.value.name}) n'est pas ouverte à la réservation.`
    }
    if (event.value.cancelled) {
      eventError.value = `L'animation n° ${geotrekId} (${event.value.name}) a été annulée. Il est impossible d'effectuer une réservation.`
    }
  } catch (error: any) {
    switch (error.message) {
      case "NOT FOUND":
        eventError.value = `L'animation n° ${geotrekId} n'a pas été trouvée. Il est impossible d'effectuer une réservation`
        break
      default:
        eventError.value = "Une erreur est survenue. Il est impossible d'effecuter une réservation. Merci de prendre contact avec le parc."
    }
  } 
  // Prefil email 
  resaToEdit.value = { email: user.value?.email } as Resa
  loadingEvent.value = false
})

const reservationOpened = computed(() => {
  if (!event.value) {
    return isReservationGloballyOpened()
  } else return isReservationOpened(event.value)
})

/**
 * Fonctions d'enregistrement de la réservation
 */
const saving = ref(false)
const saveError = ref<any>(null)
async function saveReservation(values: any) {
  status.value = STATUS.SAVING
  saving.value = true
  try {
    await postReservation({
      id_event: geotrekId,
      ...values
    })
    status.value = STATUS.SUCCESS
  } catch (error) {
    saveError.value = error
    status.value = STATUS.ERROR
  }
  saving.value = false
}

</script>