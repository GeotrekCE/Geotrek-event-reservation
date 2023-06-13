<template>
  <header class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900">
        Listing des animations
      </h1>
    </div>
  </header>


  <main class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 px-4 py-6">

    <section class="pb-12">

      <button @click="getEvents">Get events</button>

      <p-data-table
        :value="events"
        data-key="id"
        tableStyle="min-width: 50rem"
        stripedRows
        class="p-datatable-sm"
        lazy
        paginator
        :rows="10"
        :total-records="totalEvents"
        :loading="loading"
        @page="onPage"
      >
        <template #empty>Aucune animation trouvée.</template>
        <template #loadingicon>
          <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </template>
        <p-column header='Détail' field='id' sortable></p-column>
        <p-column header='Nom' field='name'></p-column>
        <p-column header='Publié' field='published'></p-column>
        <p-column header='Remplissage' field='remplissage' sortable>
          <template #body="{data}">
            <reservation-progress
              :reservation-nb="data.sum_participants"
              :participant-nb="data.capacity"
              :attente-nb="data.sum_participants_liste_attente"
            />
          </template>
        </p-column>
        <p-column header='Date de début' field='begin_date'></p-column>
        <p-column header='Date de fin' field='end_date'></p-column>
        <p-column header='Type' field='type.type'></p-column>
        <p-column header='Massif' field='massif'></p-column>
      </p-data-table>

    </section>

  </main>

  <div name="event-detail">
    <!-- 
    <v-container>
      <events-filters @search="() => {getEvents()}" />
    </v-container> -->


    <!-- <v-data-table
      :page="page"
      :pageCount="numberOfPages"
      :headers="headers"
      :items="events"
      :item-class="row_classes"
      v-model:options="options"
      :server-items-length="totalEvents"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.id="{ item }">
        <router-link :to="{ name: 'event', params: { id: item.id }}">
          <v-btn icon color="blue">
            <v-icon v-if="(item.bilan || {}).annulation">mdi-text-box-remove</v-icon>
            <v-icon v-else>mdi-text-box</v-icon>
          </v-btn>
        </router-link>
      </template>
      <template v-slot:item.name="{ item }">
        <router-link :to="{ name: 'event', params: { id: item.id }}">
          {{ item.name }}
        </router-link>
      </template>
      <template v-slot:item.published="{ item }">
        <v-simple-checkbox v-model="item.published" disabled></v-simple-checkbox>
      </template>
    </v-data-table> -->
  </div>
</template>

<script setup lang="ts">
import { getEvents } from '@/utils/appli_api';
import ReservationProgress from '@/components/ReservationProgress.vue';
// import EventsFilters from '@/components/EventsFilters.vue';
import { useEventStore } from '@/stores/events'
import { ref, onBeforeMount, watch } from 'vue'
import PDataTable from 'primevue/datatable'
import PColumn from 'primevue/column'

const eventStore = useEventStore()

const totalEvents = ref(0)
const numberOfPages = ref(0)
const events = ref<{id: string}[]>([])
const loading = ref(true)
const options = ref({
  sortBy: ['begin_date'],
  sortDesc: [false],
  page: 1,
  itemsPerPage: 10
})
const errorMessage = ref<string | null | any>(null)

async function loadEvents () {
  loading.value = true;
  const {
    page, itemsPerPage, sortBy, sortDesc
  } = options.value;
  let params = {
    limit: itemsPerPage,
    page,
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

function search() {
  options.value.page = 1;
  loadEvents();
}
function row_classes(item: any) {
  if ((item.bilan || {}).annulation) {
    return 'red lighten-3';
  }
}

async function onPage($event: any) {
  options.value.page = $event.page
  await loadEvents()
}

watch(
  () => options,
  () => {
    loadEvents()
  },
  { deep: true }
)

onBeforeMount(async () => {
  loadEvents()
})

</script>

<style>
#red {
  background-color: aquamarine;
}
</style>
