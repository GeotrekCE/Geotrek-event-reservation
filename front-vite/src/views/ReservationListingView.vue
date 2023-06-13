<template>
  <header class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900">
        Listing des réservations
      </h1>
    </div>
  </header>


  <main class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 px-4 py-6">

    <section class="pb-12">

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
        <p-column field="id_event" header="Événement"></p-column>
        <p-column field="begin_date" header="Date de début"></p-column>
        <p-column field="nom" header="Nom"></p-column>
        <p-column field="prenom" header="Prénom"></p-column>
        <p-column field="nb_moins_6_ans" header="-6 ans"></p-column>
        <p-column field="nb_6_8_ans" header="6/8 ans"></p-column>
        <p-column field="nb_9_12_ans" header="9/12 ans"></p-column>
        <p-column field="nb_adultes" header="adultes"></p-column>
        <p-column field="sum_participants" header="Total"></p-column>
        <p-column field="sum_participants_liste_attente" header="Liste d'attente"></p-column>
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

    </section>

  </main>

	
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from 'vue'
import { getReservations } from '@/utils/appli_api'

import PDataTable from 'primevue/datatable'
import PColumn from 'primevue/column'
import PTag from 'primevue/tag'

const loading = ref(false)
const resas = ref<{results: any[], total: number}>({results: [], total: 0})
const error = ref(false)

onBeforeMount(async () => loadData())

async function onPage($event: any) {
  loadData($event.page)
}

async function loadData (page = 0, sortField = null, sortOrder = null) {
  loading.value = true
  try {
    resas.value = await getReservations(page + 1, 10, sortField, sortOrder)
  } catch {
    error.value = true
  }
  loading.value = false
};

</script>