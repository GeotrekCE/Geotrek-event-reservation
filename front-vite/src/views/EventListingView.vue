<template>
  <div class="flex min-h-full flex-col">

    <header class="bg-white shadow">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold tracking-tight text-gray-900">
          Listing des animations
        </h1>
      </div>
    </header>

    <main class="flex flex-grow gap-x-4">

      <nav class="w-1/4 lg:w-1/5 bg-gray-100 shadow-xl">

        <p-data-view :value="events" paginator :rows="5">
          <template #header>
            <form @submit.prevent="search">
              <div class="w-full flex justify-between">
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
              <template v-if="formOpened">
                <p-calendar
                  v-model="filters.begin_date"
                  class="rounded-sm p-inputtext-sm"
                  placeholder="Date de début"
                />
                <p-calendar
                  v-model="filters.end_date"
                  class="rounded-sm p-inputtext-sm"
                  placeholder="Date de fin"
                />
                <p-multi-select
                  v-model="filters.massif"
                  display="chip"
                  :options="districts"
                  placeholder="Massifs"
                  class="w-full md:w-20rem rounded-sm p-inputtext-sm"
                />
                <p-multi-select
                  v-model="filters.type_id"
                  display="chip"
                  :options="eventtypes"
                  placeholder="Type"
                  class="w-full md:w-20rem rounded-sm p-inputtext-sm"
                />

                <input type="checkbox" v-model="filters['published']" />Publiées
                <input type="checkbox" v-model="filters['bilan.annulation']" />Annulées
              </template>

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
              class="flex justify-between gap-x-6 p-5 hover:bg-gray-100 hover:shadow-inner border-b border-gray-200"
              :to="{ name: ROUTES_NAMES.EVENT_DETAIL, params: { id: data.id }}"
              :class="{
                'bg-red-300': data.bilan?.annulation,
                'hover:bg-red-100': data.bilan?.annulation,
                'hover:bg-gray-100': !data.bilan?.annulation,
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
                  <p class="text-sm font-medium leading-6 text-gray-900">{{ data.type.type }}</p>
                  <p class="mt-1 truncate text-xs leading-5 text-gray-500">{{ data.massif }}</p>
                </div>
              </div>
              <div class="flex flex-col gap-y-4 min-w-1/2 items-end">
                <reservation-progress
                  class="w-full"
                  :reservation-nb="data.sum_participants"
                  :participant-nb="data.capacity"
                  :attente-nb="data.sum_participants_liste_attente"
                />
                {{ data.begin_date || '?' }} - {{ data.end_date || '?' }}
              </div>
            </router-link>
          </template>
        </p-data-view>

      </nav>

      <section class="w-3/4 lg:w-4/5 " v-if="selectedEvent">

        <p-card class="rounded-sm mt-8 mx-auto max-w-6xl">
          <template #title>
            <div class="flex items-center justify-between">
              {{ selectedEvent.name }}
              <div class="text-center ml-auto text-sm font-medium">
                <a
                  :href="config.URL_GTR + '/event/' + selectedEvent.id"
                  target="_blank"
                  class="mr-2 bg-cyan-500 p-2 rounded-sm drop-shadow-md text-black"
                  :disabled="selectedEvent.published !== true">
                  Destination cévennes <i class="pi pi-external-link" />
                </a>
                <a
                  :href="config.URL_GTA + '/touristicevent/' + selectedEvent.id"
                  target="_blank"
                  class="bg-green-500 p-2 rounded-sm drop-shadow-md text-black"
                >
                  Geotrek admin <i class="pi pi-external-link" />
                </a>
              </div>

              <!-- <event-cancel-form
                :bilan="selectedEvent.bilan"
                :canceled="selectedEventCanceled"
                :id_event="selectedEvent.id"
                @submit="cancelAnimation"
                class="ml-auto"
              ></event-cancel-form> -->
              <button
                class="ml-2 rounded-sm px-3 py-2 text-sm font-medium text-white drop-shadow-md bg-red-600 hover:bg-red-400"
              >
                <i class="pi pi-exclamation-triangle" /> {{ selectedEventCanceled ? 'Dé annuler' : 'Annuler' }}
              </button>
            </div>
          </template>

          <template #content>

            <div v-if="selectedEventCanceled === true" class="bg-red-300 max-w-xl mx-auto mb-12 p-2">
              <h2 class="text-red font-medium text-xl">Animation annulée</h2>
              <div>
                <strong> Raison: </strong>
                <span>{{ selectedEvent.bilan.raison_annulation }}</span>
              </div>
            </div>

            <div v-html='selectedEvent.description_teaser'></div>

            <p-tab-view>
              <p-tab-panel header="Résumé">
                <div class="grid grid-cols-1 sm:grid-cols-6 gap-x-2 gap-y-4 mt-4" v-if="selectedEvent">
                  <div class="col-span-1 sm:col-span-3">
                    <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
                      Type
                    </label>
                    <div class="mt-2">
                      <div
                        class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
                      >
                        <span
                          class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
                        >
                          {{ ( selectedEvent.type && selectedEvent.type.type ) || 'Non renseigné' }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div class="col-span-1 sm:col-span-3">
                    <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
                      Date de début
                    </label>
                    <div class="mt-2">
                      <div
                        class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
                      >
                        <span
                          class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
                        >
                          {{ formatDate(selectedEvent.begin_date) || 'Non renseigné' }}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="col-span-1 sm:col-span-3">
                    <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
                      Date de fin
                    </label>
                    <div class="mt-2">
                      <div
                        class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
                      >
                        <span
                          class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
                        >
                          {{ formatDate(selectedEvent.end_date) || 'Non renseigné' }}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="col-span-1 sm:col-span-3">
                    <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
                      Capacité
                    </label>
                    <div class="mt-2">
                      <div
                        class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
                      >
                        <span
                          class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
                        >
                          {{ selectedEvent.capacity || 'Non renseigné' }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div class="col-span-1 sm:col-span-3">
                    <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
                      Massif
                    </label>
                    <div class="mt-2">
                      <div
                        class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
                      >
                        <span
                          class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
                        >
                          {{ selectedEvent.massif || 'Non renseigné' }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div class="col-span-full">
                    <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Informations pratiques (fr)</label>
                    <div class="mt-2">
                      <textarea id="about" name="about" rows="3" class="block w-full rounded-sm border-0 p-2 text-gray-600 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6" :value="selectedEvent.practical_info_fr" disabled />
                    </div>
                  </div>

                  <div class="col-span-full">
                    <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Informations pratiques (en)</label>
                    <div class="mt-2">
                      <textarea id="about" name="about" rows="3" class="block w-full rounded-sm border-0 p-2 text-gray-600 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6" :value="selectedEvent.practical_info_en" disabled />
                    </div>
                  </div>

                </div>

                <div
                  v-if="selectedEvent.published === true && gtevent"
                  class="grid grid-cols-1 sm:grid-cols-6 gap-x-2 gap-y-4 mt-4"
                >
                  <h2 class="col-span-full cursor-pointer" @click="showMore = !showMore">
                    <i
                      class="w-4 h-4 pi"
                      :class="{
                        'pi-chevron-down': showMore,
                        'pi-chevron-right': !showMore
                      }"
                    />
                    Données GeoTrek
                    {{ showMore ? '' : '(Cliquez pour afficher)'}}
                  </h2>
                  <template v-if="showMore">
                    <div
                      class="col-span-1 sm:col-span-3"
                      v-for="(field, index) in getGtFields(true)"
                      :key="index"
                    >
                      <label class="block text-sm font-medium leading-6 text-gray-900">{{ field.label }} : </label>
                      <span v-html="getGtFieldValue(index)"></span>
                    </div>
                    <div
                      class="col-span-1 sm:col-span-3"
                      v-for="(field, index) in getGtFields(false)"
                      :key="index"
                    >
                      <label class="block text-sm font-medium leading-6 text-gray-900">{{ field.label }} : </label>
                      <span v-html="getGtFieldValue(index)"></span>
                    </div>
                  </template>
                </div>

              </p-tab-panel>
              <p-tab-panel header="Réservations">

                <reservation-progress
                  :reservation-nb="selectedEvent.sum_participants"
                  :participant-nb="selectedEvent.capacity"
                  :attente-nb="selectedEvent.sum_participants_liste_attente"
                />
<!--                 
                <p-button color="primary" dark class="mb-2" v-bind="editedItem" @click="addItem"
                  v-show="reservationOpened" key="res_open">
                  Nouvelle réservation
                </p-button>

                <div v-show="!reservationOpened">
                  <span class="grey lighten-2 text-center px-2">
                    Réservation non ouverte
                  </span>
                </div>
 -->
                <p-data-table
                  :value="resas.results"
                  data-key="id_reservation"
                  tableStyle="min-width: 50rem"
                  stripedRows
                  class="p-datatable-sm"
                  lazy
                  paginator
                  :rows="10"
                  :total-records="resas.total"
                  :loading="loading"
                  @page="onPage($event)"
                >
                  <template #empty>Aucune réservation trouvée.</template>
                  <template #loadingicon>
                    <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
                  </template>
                  <p-column field="nom" header="Nom"></p-column>
                  <p-column field="prenom" header="Prénom"></p-column>
                  <p-column field="sum_participants" header="Total"></p-column>
                  <p-column field="sum_participants_liste_attente" header="Liste d'attente"></p-column>
                  <p-column field="nb_adultes" header="adultes"></p-column>
                  <p-column field="nb_moins_6_ans" header="-6 ans"></p-column>
                  <p-column field="nb_6_8_ans" header="6/8 ans"></p-column>
                  <p-column field="nb_9_12_ans" header="9/12 ans"></p-column>
                  <p-column field="nb_plus_12_ans" header="+12 ans"></p-column>
                  <p-column field="confirmed" header="Confirmé">
                    <template #body="{ data }">
                        <i
                          class="pi"
                          :class="{ 'pi-check-circle text-green-500': data.confirmed, 'pi-times-circle text-orange-400': !data.confirmed }"
                        />
                    </template>
                  </p-column>
                  <p-column field="confirmed" header="Statut">
                    <template #body="{ data }">
                      <p-tag
                        class="rounded-sm"
                        :value="data.confirmed ? 'Confirmé' : 'En attente'"
                        :severity="data.confirmed ? 'success' : 'warning'"
                      />
                    </template>
                  </p-column>
                  <p-column header="Annulation">
                    <template #body>
                      <button
                        class="rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-600 bg-sky-600 hover:bg-sky-500"
                      >Annuler</button>
                    </template>
                  </p-column>
                </p-data-table>
              </p-tab-panel>
              <p-tab-panel header="Bilan">
                <event-bilan
                  v-if="!selectedEventCanceled"
                  :event="selectedEvent"
                  @reloadEvent="getEvent()"
                />
                <div v-else>
                  <v-alert text dense icon="mdi-information-outline" border="left">
                    L'animation a été annulée, il n'y a pas de bilan à saisir
                  </v-alert>
                </div>
              </p-tab-panel>
            </p-tab-view>
          </template>
        </p-card>
          <!-- 
          <div v-if="selectedEvent.published === true">
            <gt-event-detail class="mb-10" :id="id" :published="selectedEvent.published"></gt-event-detail>
          </div>
          -->
      </section>

      <section class="w-3/4 grid min-h-full px-6 py-24 sm:py-32 lg:px-8" v-else>

        <div class="text-center">
          <p class="mt-6 text-base leading-7 text-gray-600">Merci de sélectioner une animation dans la liste de gauche.</p>
        </div>        

      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { getEvents, getReservations } from '@/utils/appli_api';
import ReservationProgress from '@/components/ReservationProgress.vue';
import { useEventStore } from '@/stores/events'
import { ref, onBeforeMount, watch, computed } from 'vue'

import PDataView from 'primevue/dataview'
import PCalendar from 'primevue/calendar'
import PInputText from 'primevue/inputtext'
import PMultiSelect from 'primevue/multiselect'
import PCard from 'primevue/card'
import PTabView from 'primevue/tabview'
import PTabPanel from 'primevue/tabpanel'
import PDataTable from 'primevue/datatable'
import PColumn from 'primevue/column'
import PTag from 'primevue/tag'

import { ROUTES_NAMES } from '@/router'
import type { ResaEventFilters } from '@/declaration';
import { getDistricts, getTouristiceventType, getTouristicEventDetail } from '@/utils/gta_api';

import { formatDate } from '@/utils/formatDate'
import { gtApiFields, type API_FIELDS } from '@/utils/fields'
import type { ResaBilan } from '@/declaration';

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
 * Donnée unitaire d'un événement
 */
const selectedEvent = ref<any>(null)
const selectedEventCanceled = computed(() => selectedEvent.value?.bilan?.annulation)
const gtevent = ref<any>(null)
const resas = ref<any>(null)
const showMore = ref(false)
const bilan = ref<ResaBilan | null>(null)
/**
 * Fonction de chargement des événements
 */
async function loadEvents () {
  loading.value = true;
  const {
    page, itemsPerPage, sortBy, sortDesc
  } = options.value;
  let params = {
    limit: itemsPerPage,
    page: page + 1,
    sortBy,
    sortDesc
  };
  params = { ...params, ...eventStore.filters }
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
async function loadGTEvent () {
  gtevent.value = await getTouristicEventDetail(selectedEvent.value.id)
}
function search() {
  options.value.page = 0;
  loadEvents();
}
async function loadReservations (page: number = 0) {
  resas.value = []
  resas.value = await getReservations({
    page: page + 1,
    event_id: selectedEvent.value.id 
  }) 
}
function onPage($event: any) {
  loadReservations($event.page)
}

/*async function cancelAnimation() {
  editedItem.id_numerisateur = user.id_role;
  editedItem.id_event = id_event;
  if (editedItem.annulation === false) {
    editedItem.raison_annulation = '';
  }
  postBilan(editedItem)
}*/

/**
 * Fonction de gestion des champs geotrek
 */
function getGtFields(main: boolean): API_FIELDS {
  return Object.keys(gtApiFields)
    .filter((key) => gtApiFields[key].main === main)
    .reduce((res, key) => ({ ...res, [key]: gtApiFields[key] }), {});
}

function getGtFieldValue(field: string) {
  return field.split('.').reduce(
    (subevent, c) => ((c in subevent) ? subevent[c] : subevent),
    gtevent.value
  );
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

watch(selectedEvent, () => {
  loadGTEvent()
  loadReservations()
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
  eventtypes.value = eventtypesResponse.results.map((item: any) => item.name)
})

</script>

<style>
#red {
  background-color: aquamarine;
}
</style>
