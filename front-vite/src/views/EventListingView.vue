<template>
  <div class="flex min-h-full flex-col">

    <header class="hidden md:block bg-white shadow">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold tracking-tight text-gray-900">
          Listing des animations
        </h1>
      </div>
    </header>

    <main class="flex flex-grow gap-x-4">

      <nav
        class="md:block w-full md:w-1/4 bg-gray-100 shadow-xl"
        :class="{ hidden: selectedEvent }"
      >

        <p-data-view
          :value="events"
          paginator
          :rows="5"
          data-key="id"
          @page="onPageDataView"
        >
          <template #header>
            <form @submit.prevent="search">
              <div class="w-full flex justify-between mb-4">
                <span class="p-input-icon-right w-full">
                  <i class="pi pi-search" />
                  <p-input-text
                    v-model="filters.search_name"
                    class="rounded-sm w-full p-inputtext-sm"
                    placeholder="Nom animation"
                  />
                </span>
                <button
                  v-if="!formOpened"
                  type="submit"
                  class="rounded-sm ml-2 px-3 py-2 text-sm font-medium text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-600"
                  :class="{
                    'bg-sky-600': !loading,
                    'hover:bg-sky-500': !loading,
                    'bg-sky-100': loading,
                    'hover:bg-sky-100': loading,
                    'text-black': loading,
                  }"
                  :disabled="loading"
                >
                  <i
                    class="pi"
                    :class="{ 'pi-search': !loading, 'pi-spinner pi-spin': loading }"
                  />
                </button>
              </div>
              <div v-if="formOpened" class="space-y-4">
                <p-calendar
                  v-model="filters.begin_date"
                  class="rounded-sm p-inputtext-sm w-64 mr-2"
                  placeholder="Date de début"
                  dateFormat="dd/mm/yy"
                  showIcon
                  showButtonBar
                />
                <p-calendar
                  v-model="filters.end_date"
                  class="rounded-sm p-inputtext-sm w-64"
                  placeholder="Date de fin"
                  dateFormat="dd/mm/yy"
                  showIcon
                  showButtonBar
                />
                <p-multi-select
                  v-model="filters.massif"
                  display="chip"
                  :options="districts"
                  placeholder="Massifs"
                  class="rounded-sm p-inputtext-sm w-64 mr-2"
                />
                <p-multi-select
                  v-model="filters.type_id"
                  display="chip"
                  :options="eventtypes"
                  data-key="id"
                  option-label="name"
                  option-value="id"
                  placeholder="Type"
                  class="rounded-sm p-inputtext-sm w-64"
                />

                <div class="flex items-center">
                  <input type="checkbox" v-model="filters['published']" class="mr-2" />
                  <label>Publiées</label>
                </div>

                <div class="flex items-center">
                  <input type="checkbox" v-model="filters['cancelled']" class="mr-2" />
                  <label>Annulées</label>
                </div>

              </div>

              <div class="w-full flex justify-between items-end">
                <button
                  @click="formOpened = !formOpened"
                  class="rounded-sm text-sm p-2 ml-auto"
                >
                  {{ formOpened ? 'Moins de détail' : 'Plus de détail' }}
                </button>

                <button
                  v-if="formOpened"
                  type="submit"
                  class="rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-600"
                  :class="{
                    'bg-sky-600': !loading,
                    'hover:bg-sky-500': !loading,
                    'bg-sky-100': loading,
                    'hover:bg-sky-100': loading,
                    'text-black': loading,
                  }"
                  :disabled="loading"
                >
                  {{ loading ? 'Recherche en cours...' : 'Rechercher' }}
                </button>
              </div>

            </form>

          </template>
          <template #list="{ data }">
            <router-link
              class="flex justify-between gap-x-6 p-5 hover:bg-gray-200 hover:shadow-inner border-b border-gray-200"
              :to="{ name: ROUTES_NAMES.EVENT_DETAIL, params: { id: data.id }}"
              :class="{
                'bg-red-300 hover:bg-red-100': data.bilan?.annulation || data.cancelled,
                'hover:bg-gray-100': !data.bilan?.annulation && !data.cancelled,
                'bg-gray-100 shadow-inner border-r-4 border-solid border-gray-500 border-b-0': data.id === selectedEvent?.id,
                'bg-red-200 border-red-500': (data.bilan?.annulation || data.cancelled) && data.id === selectedEvent?.id,
              }"
              @click="selectedEvent = data"
            >
              <div class="flex flex-col gap-x-4">
                <span>
                  <i
                    class="pi"
                    :class="{ 'pi-check-circle text-green-500': data.published, 'pi-times-circle text-orange-400': !data.published }"
                  />
                  {{ data.name }}
                </span>
                <div class="min-w-0 flex-auto">
                  <p class="text-sm font-medium leading-6 text-gray-900">{{ data.type?.type }}</p>
                  <p class="mt-1 truncate text-xs leading-5 text-gray-500">{{ data.massif }}</p>
                </div>
              </div>
              <div class="flex flex-col gap-y-4 min-w-1/2 items-end">
                <reservation-progress
                  class="w-full"
                  :reservation-nb="data.sum_participants"
                  :participant-nb="data.capacity"
                  :attente-nb="data.sum_participants_liste_attente"
                  :display-text="false"
                />
                {{ formatDate(data.begin_date) || '?' }} 
                <span v-if="data.end_date">
                  - {{ formatDate(data.end_date) }}
                </span>
              </div>
            </router-link>
          </template>
        </p-data-view>

      </nav>

      <section class="w-full md:w-3/4" v-if="selectedEvent">

        <div class="md:hidden h-12 flex items-center cursor-pointer" @click="selectedEvent = null">
          <i class="pi pi-chevron-left" />Retourner au résultats
        </div>

        <p-card class="rounded-sm md:mt-8 mx-auto max-w-6xl">
          <template #title>
            <div class="md:flex items-center justify-between space-y-4">
              {{ selectedEvent.name }}
              <div class="text-center md:ml-auto text-sm font-medium mt-4 md:mt-0">
                <a
                  :href="config.URL_GTR + '/event/' + selectedEvent.id"
                  target="_blank"
                  class="mr-2 bg-cyan-500 text-gray-900 p-2 rounded-sm drop-shadow-md text-black"
                  :disabled="selectedEvent.published !== true">
                  Geotrek <i class="pi pi-external-link" />
                </a>
                <a
                  :href="config.URL_GTA + '/touristicevent/' + selectedEvent.id"
                  target="_blank"
                  class="bg-green-500 text-gray-900 p-2 rounded-sm drop-shadow-md text-black"
                >
                  Geotrek admin <i class="pi pi-external-link" />
                </a>
              </div>

            </div>
          </template>

          <template #content>

            <div v-if="selectedEventCanceled === true" class="bg-red-300 max-w-xl mx-auto mb-12 p-2">
              <h2 class="text-red font-medium text-xl">Animation annulée</h2>
              <div>
                <strong> Raison: </strong>
                <span>{{ selectedEvent.bilan?.raison_annulation }}</span>
              </div>
            </div>

            <div v-html='selectedEvent.description_teaser'></div>

            <p-tab-view>
              <p-tab-panel header="Résumé">

                <event-summary
                  :event="selectedEvent"
                  :gtevent="gtevent"
                />

              </p-tab-panel>
              <p-tab-panel header="Réservations">

                <reservation-progress
                  class="my-4"
                  :reservation-nb="selectedEvent.sum_participants"
                  :participant-nb="selectedEvent.capacity"
                  :attente-nb="selectedEvent.sum_participants_liste_attente"
                />

                <div class="my-4 text-center">
                  <button
                    class="rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm bg-sky-600 hover:bg-sky-500"
                    v-if="reservationOpened && statutReservation === 'list'"
                    @click="statutReservation = 'form'"
                  >
                    Créer une nouvelle réservation
                  </button>

                  <p-message
                    severity="info"
                    :closable="false"
                    v-else-if="!reservationOpened"
                    class="rounded-sm"
                  >
                    <p class="ml-4">Réservation non ouverte</p>
                  </p-message>
                </div>

                <event-reservations
                  v-if="statutReservation === 'list'"
                  :loading="loading"
                  :resas="resas"
                  :id-event="selectedEvent.id"
                  @page="onPageReservations"
                  @cancel="onCancelReservation"
                  @confirm="onConfirmReservation"
                  @edit="onEditReservation"
                />

                <event-reservation-form
                  v-else-if="statutReservation === 'form'"
                  class="mt-4"
                  @submit="onSubmitReservation"
                  @cancel="onCloseReservation"
                  :saving="saving"
                  :save-error="saveError"
                  :display-cancel="true"
                  :original-values="resaToEdit || {}"
                  :display-admin-fields="true"
                />

              </p-tab-panel>
              <p-tab-panel header="Bilan">

                <p-message
                  severity="warn"
                  :closable="false"
                  class="rounded-sm"
                >
                  <p class="ml-4">La saisie du bilan est réservée à l'animateur</p>
                </p-message>

                <div v-if="selectedEventCanceled">
                  <p-message
                    severity="error"
                    :closable="false"
                    class="rounded-sm"
                  >
                    <p class="ml-4">L'animation a été annulée, il n'y a pas de bilan à saisir</p>
                  </p-message>
                </div>

                <div
                  v-else-if="selectedEvent.bilan && !bilanEditing"
                  class="grid grid-cols-1 sm:grid-cols-10 gap-x-2 gap-y-4 mt-4"
                >
                  <div
                    class="col-span-1 sm:col-span-2"
                    v-for="(field, index) in fieldsClasseAge"
                    :key="index"
                  >
                    <label class="block text-sm font-medium leading-6 text-gray-900">{{ field }} : </label>
                    <span>{{ selectedEvent.bilan[index] }}</span>
                  </div>

                  <div class="col-span-full">
                    <label class="block text-sm font-medium leading-6 text-gray-900">Commentaire : </label>
                    <p
                      v-for="comment in selectedEvent.bilan?.commentaire?.split('\n')"
                      :key="comment"
                    >
                      {{comment }}
                    </p>
                  </div>

                  <div class="col-span-full flex items-center">
                    <button
                      class="ml-auto rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-600 bg-sky-600 hover:bg-sky-500"
                      @click="bilanEditing = true"
                    >
                      Modifier le bilan
                    </button>
                  </div>
                </div>

                <div class="border-b border-gray-900/10 pb-12" v-else>

                  <event-bilan-form
                    :saving="bilanSaving"
                    :error="bilanError"
                    :original-data="selectedEvent.bilan"
                    @submit="onSaveBilan"
                  />

                </div>

              </p-tab-panel>
              <p-tab-panel>
                <template #header>
                  <span class="text-red-500 p-tabview-title">
                    Annulation
                  </span>
                </template>

                <p-message severity="warn" :closable="false">
                  <div class="space-y-4 ml-4">
                    <p>L'annulation d'une animation doit d'abord être faite dans GeoTrek.</p>
                    <p>À partir de l'outil de réservation, l'annulation va déclencher l'envoi d'un mail à tous les inscrits
                    pour leur préciser l'annulation de l'animation.</p>
                  </div>
                </p-message>

                <event-cancel-form
                  :raison-annulation="selectedEvent.bilan?.raison_annulation"
                  :annulation="selectedEventCanceled"
                  @submit="onSaveBilan"
                />
              </p-tab-panel>
            </p-tab-view>
          </template>
        </p-card>
      </section>

      <section class="hidden md:block md:w-3/4 2xl:w-4/5 grid min-h-full px-6 py-24 sm:py-32 lg:px-8" v-else>

        <div class="text-center">
          <p class="mt-6 text-base leading-7 text-gray-600">Merci de sélectioner une animation dans la liste de gauche.</p>
        </div>        

      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import {
  getEvents,
  getReservations,
  postBilan,
  getEvent,
  deleteReservation,
  updateReservation,
  postReservation
} from '@/utils/appli_api';
import ReservationProgress from '@/components/ReservationProgress.vue';
import EventBilanForm from '@/components/EventBilanForm.vue'
import EventCancelForm from '@/components/EventCancelForm.vue'
import EventSummary from '@/components/EventSummary.vue'
import EventReservations from '@/components/EventReservations.vue'
import EventReservationForm from '@/components/EventReservationForm.vue'
import { useEventStore } from '@/stores/events'
import { ref, onBeforeMount, watch, computed } from 'vue'

import PDataView from 'primevue/dataview'
import PCalendar from 'primevue/calendar'
import PInputText from 'primevue/inputtext'
import PMultiSelect from 'primevue/multiselect'
import PCard from 'primevue/card'
import PTabView from 'primevue/tabview'
import PTabPanel from 'primevue/tabpanel'
import PMessage from 'primevue/message'

import { ROUTES_NAMES } from '@/router'
import type { ResaEventFilters, ResaBilan, Resa } from '@/declaration';
import { getDistricts, getTouristiceventType, getTouristicEventDetail } from '@/utils/gta_api';

import { formatDate } from '@/utils/formatDate'
import { fieldsClasseAge } from '@/utils/fields'

const eventStore = useEventStore()

/**
 * Données des événements / animations
 */
const totalEvents = ref(0)
const numberOfPages = ref(0)
const events = ref<{id: string}[]>([])
const loading = ref(true)
const options = ref({
  sortBy: ['begin_date'],
  sortDesc: [false],
  page: 0,
  itemsPerPage: 10
})
const errorMessage = ref<string | null | any>(null)
const config = ref(CONFIGURATION)

/**
 * Formulaire de recherche des événements / animations
 */
const filters = ref<ResaEventFilters>({
  search_name: '',
  begin_date: '',
  end_date: '',
  type_id: [],
  massif: []
})
const defaultFilters =ref<ResaEventFilters>({
  begin_date: '',
  end_date: '',
  type_id: [],
  massif: [],
  search_name: ''
})
const districts = ref<string[]>([])
const eventtypes = ref<string[]>([])
const formOpened = ref(false)

/**
 * Gestion d'un événement
 */
const selectedEvent = ref<any>(null)
const selectedEventCanceled = computed(() => selectedEvent.value?.cancelled || selectedEvent.value?.bilan?.annulation)
const gtevent = ref<any>(null)
const resas = ref<any>({ results: [], total: 0 })

/**
 * Est ce que la réservation est ouverte
 * pour l'événement courant ?
 * 
 * Si événement / animation annulée => non
 * 
 * Si événement / animation passée => non
 * 
 * Si période de réservation trop courte => non
 * 
 * Cela dépend s'il est passé => non
 * et s'il on est dans une période correcte
 * ATTENTION: changement au niveau de l'algo pour le PNG,
 * le PNG préfère utiliser une date à partir de laquelle toutes les résas sont possibles,
 * et pas sur une période glissante...
 */
const reservationOpened = computed(() => {

  if (selectedEvent.value.cancelled) return false

  // If event is in past
  if (new Date().setHours(0, 0, 0, 0) > new Date(selectedEvent.value.begin_date).setHours(0, 0, 0, 0)) {
    return false
  }

  // If event in reservation period (control by DAY_BEFORE_RESA)
  if ((CONFIGURATION.DAY_BEFORE_RESA || -1) !== -1) {
    const resaBeginDate = new Date(selectedEvent.value.begin_date);
    resaBeginDate.setDate(resaBeginDate.getDate() - CONFIGURATION.DAY_BEFORE_RESA);
    if (new Date().setHours(0, 0, 0, 0) >= resaBeginDate.setHours(0, 0, 0, 0)) {
      return true;
    }
    return false;
  }

  return true;
})

/**
 * Fonction de chargement des événements
 */
async function loadEvents () {
  loading.value = true;
  const {
    page, itemsPerPage, sortBy, sortDesc
  } = options.value;
  let params: Record<string, any> = {
    limit: itemsPerPage,
    page: page + 1,
    sortBy,
    sortDesc
  };
  Object.keys(filters.value).forEach((key: string) => {
    const currentValue = filters.value[key as keyof ResaEventFilters]
    if (currentValue) {
      params[key] = currentValue
      if (currentValue instanceof Date) {
        params[key] = currentValue.toISOString()
      }
    } 
  })
  try {
    const data = await getEvents(params)
    events.value = data.results;
    totalEvents.value = data.total;
    numberOfPages.value = data.total / data.limit;
    loading.value = false;
  } catch (error) {
    errorMessage.value = error;
    console.error('There was an error!', error);
  }
}
function search() {
  options.value.page = 0;
  loadEvents();
}
function onPageDataView($event: any) {
  options.value.page = $event.page
  loadEvents()
}
async function loadReservations (page: number = 0) {
  resas.value = { results: [], total: 0 }
  resas.value = await getReservations({
    page: page + 1,
    event_id: selectedEvent.value.id 
  }) 
}
function onPageReservations($event: any) {
  loadReservations($event.page)
}
async function onCancelReservation(id_reservation: number) {
  await deleteReservation(id_reservation)
  await loadReservations(options.value.page)
}
async function onConfirmReservation(id_reservation: number) {
  await updateReservation(id_reservation, { confirmed: true })
  await loadReservations(options.value.page)
}
function onEditReservation(id_reservation: number) {
  const currentResa = resas.value.results?.find((r: Resa) => r.id_reservation === id_reservation)
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { event, ...rest } = currentResa
  resaToEdit.value = rest

  statutReservation.value = 'form'
}

/**
 * Gestion du bilan
 */
const bilanSaving = ref(false)
const bilanError = ref<any>(null)
const bilanEditing = ref(false)
async function onSaveBilan(data: Partial<ResaBilan>) {
  bilanSaving.value = true
  bilanError.value = null
  try {
    await postBilan({
      id_event: selectedEvent.value.id,
      id_bilan: selectedEvent.value.bilan?.id_bilan,
      ...data
    })
    selectedEvent.value = await getEvent(selectedEvent.value.id)
    const eventIndex = events.value.findIndex(r => r.id === selectedEvent.value.id)
    events.value[eventIndex] = selectedEvent.value
    bilanEditing.value = false
  } catch (error) {
    bilanError.value = error
  }
  bilanSaving.value = false
}


/**
 * Fonctions d'enregistrement de la réservation
 */
const statutReservation = ref<'list' | 'form'>('list')
const saving = ref(false)
const saveError = ref<any>(null)
const resaToEdit = ref<Resa | null>(null)
async function onSubmitReservation({ liste_attente, ...values }: Partial<Resa>) {
  saving.value = true
  saveError.value = null
  try {
    if (resaToEdit.value?.id_reservation) {
      await updateReservation(resaToEdit.value?.id_reservation, {
        liste_attente,
        ...values
      })
    } else {
      await postReservation({
        id_event: selectedEvent.value.id,
        ...values
      })
    }
    await loadReservations()
    statutReservation.value = 'list'
  } catch (error) {
    saveError.value = error
  }
  saving.value = false
}
function onCloseReservation() {
  statutReservation.value = 'list'
  resaToEdit.value = null
}

/**
 * On fraîchit les events si un élément des options change
 */
watch(
  () => options,
  () => {
    loadEvents()
  },
  { deep: true }
)

watch(selectedEvent, async () => {
  await loadReservations()
  gtevent.value = await getTouristicEventDetail(selectedEvent.value.id)
})

/**
 * Chargement initial : événements + glossaires
 */
onBeforeMount(async () => {
  loadEvents()
  filters.value = defaultFilters.value;
  const districtsResponse = await getDistricts()
  districts.value = districtsResponse.results.map((item: any) => item.name)
  const eventtypesResponse = await getTouristiceventType()
  eventtypes.value = eventtypesResponse.results.map((item: any) => ({
    id: item.id,
    name: item.type.fr
  }))
})

</script>

<style>
.p-tabview .p-tabview-panel, 
.p-tabview .p-tabview-panels{
  margin: 0;
  padding: 0;
}

.p-tabview .p-tabview-nav li.p-highlight .p-tabview-nav-link {
  color: var(--blue-500);
  border-color: var(--blue-500);
}
.p-tabview .p-tabview-nav li .p-tabview-nav-link:not(.p-disabled):focus {
  box-shadow: unset;
}
</style>
