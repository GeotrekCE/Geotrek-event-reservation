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

      <div v-html="markdownToHTML" class="my-8 text-base leading-7 text-gray-900 space-y-4"></div>
    
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
        v-model:expandedRows="expandedRows"
        @row-expand="onRowExpand"
      >
        <template #empty>Aucune réservation trouvée.</template>
        <template #loadingicon>
          <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </template>
        <p-column frozen expander />
        <p-column frozen field="event.name" header="Événement"></p-column>
        <p-column field="event.begin_date" header="Date">
          <template #body="{data}">
            {{ formatDate(data.event?.begin_date)}}
          </template>
        </p-column>
        <p-column field="nb_adultes" header="adultes"></p-column>
        <p-column field="nb_moins_6_ans" header="-6 ans"></p-column>
        <p-column field="nb_6_8_ans" header="6/8 ans"></p-column>
        <p-column field="nb_9_12_ans" header="9/12 ans"></p-column>
        <p-column field="nb_plus_12_ans" header="+12 ans"></p-column>
        <p-column field="confirmed" header="Statut">
          <template #body="{ data }">

            <p-tag
              class="rounded-sm"
              v-if="data.cancelled"
              value="Annulée"
              severity="danger"
            />
            <p-tag
              class="rounded-sm"
              v-else-if="!data.confirmed"
              value="À confirmer"
              severity="warning"
            />
            <p-tag
              class="rounded-sm"
              v-else-if="data.liste_attente === null"
              value="Non traité"
              severity="info"
            />
            <p-tag
              class="rounded-sm"
              v-else-if="data.liste_attente"
              value="Liste d'attente"
              severity="warning"
            />
            <p-tag
              class="rounded-sm"
              v-else-if="!data.liste_attente"
              value="OK"
              severity="success"
            />
          </template>
        </p-column>
        <p-column header="Actions">
          <template #body="{ data }">
            <button
              class="rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm bg-sky-600 hover:bg-sky-500"
              @click="onCancelResa($event, data.id_reservation)"
              v-if="!data.cancelled"
            >Annuler</button>
          </template>
        </p-column>

        <template #expansion="{ data }">
          <div class="grid grid-cols-1 sm:grid-cols-10 gap-x-2 gap-y-4 mt-4">
            <div
              v-for="(field) in expandedFields"
              :key="field.name"
              :class="field.class"
            >
              <label class="block text-sm font-medium leading-6 text-gray-900">{{ field.label }} : </label>
              <span v-if="field.name !== 'commentaire'">{{ data[field.name] }}</span>
              <template v-else>
                <p
                  v-for="comment in data[field.name]?.split('\n')"
                  :key="comment"
                >
                  {{comment }}
                </p>
              </template>

            </div>
            <div v-if="data.infos" class="col-span-full">
              <label class="block text-sm font-medium leading-6 text-gray-900">Informations de rendez-vous : </label>
              <template v-if="data.infos.info_rdv">
                <p
                  v-for="comment in data.infos.info_rdv?.split('\n')"
                  :key="comment"
                >
                  {{comment }}
                </p>
              </template>
              <p v-else>
                Aucune information à ce jour
              </p>
            </div>
          </div>
        </template>

      </p-data-table>

    </section>

  </main>

	
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from 'vue'
import { getReservations, deleteReservation, getEventInfo } from '@/utils/appli_api'
import { formatDate } from '@/utils/formatDate'
import { marked } from 'marked';
import { expandedFields } from '@/utils/fields'

import PDataTable from 'primevue/datatable'
import PColumn from 'primevue/column'
import PTag from 'primevue/tag'
import { useConfirm } from "primevue/useconfirm";

const confirm = useConfirm()

const loading = ref(false)
const resas = ref<{results: any[], total: number}>({results: [], total: 0})
const error = ref(false)

const markdownToHTML = ref('')

const expandedRows = ref([])

onBeforeMount(async () => {
  loadData()
  const response = await fetch('page_reservation.md')
  const text = await response.text()
  markdownToHTML.value = marked(text) || 'Erreur lors de la récupération des informations à afficher.'

})

async function onPage($event: any) {
  loadData($event.page)
}

async function loadData (page = 0, sortField = null, sortOrder = null) {
  loading.value = true
  try {
    resas.value = await getReservations({
      page: page + 1, 
      limit: 10, 
      sortBy: sortField, 
      sortOrder,
    })
  } catch {
    error.value = true
  }
  loading.value = false
};

function onCancelResa(event: any, id_reservation: number) {
  confirm.require({
    target: event.currentTarget,
    message: 'Êtes vous sûr de vouloir annuler cette réservation ?',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Oui',
    rejectLabel: 'Non',
    async accept () {
      await deleteReservation(id_reservation)
      await loadData()
    },
  })
}

async function onRowExpand(event: any) {
  console.log(event.data.id_event)
  const infos = await getEventInfo(event.data.id_event)
  event.data.infos = {
    info_rdv: infos.info_rdv
  }
}

</script>