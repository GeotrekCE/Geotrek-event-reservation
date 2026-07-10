<template>
  <div class="flex min-h-full flex-col">
    <header class="hidden md:block shadow">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
          Liste des emails envoyés
        </h1>
      </div>
    </header>

    <main class="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8">
      <section class="mx-auto">
        <div v-if="errorStats" class="text-red-500">
          Une erreur est survenue :
          <p>{{ errorStats }}</p>
        </div>
      </section>

      <section class="mx-auto" v-if="!loading">
        <div class="flex justify-between">
          <Button
            type="button"
            icon="pi pi-filter-slash"
            label="Réinitialiser les filtres"
            outlined
            @click="clearFilter()"
          />
          <IconField>
            <InputIcon>
              <i class="pi pi-search" />
            </InputIcon>
            <InputText
              v-model="filters['global'].value"
              placeholder="Rechercher"
            />
          </IconField>
        </div>

        <p-data-table :value="logs"
          :globalFilterFields="[
            (v) =>
              formatDateTimeString(v.date),
            'subject',
            'email'
          ]"
          v-model:filters="filters"
          stripedRows
          class="p-datatable-sm mt-6"
          tableStyle="min-width: 50rem"
          paginator
          scrollable
          :rows="10"
          :rowsPerPageOptions="[10, 20, 50, 100]"
          currentPageReportTemplate="[ Éléments {first} à {last} sur {totalRecords} ]"
          :paginatorTemplate="{
            default: 'CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown'
          }"
          :loading="loading"
          filterDisplay="row"
          sortField="date"
          :sortOrder="-1"
        >
            <p-column field="date" header="Date" sortable
              :showFilterMenu="false"
            >
              <template #filter="{ filterModel, filterCallback }">
                <InputText
                  v-model="filterModel.value"
                  type="text"
                  @input="filterCallback()"
                  class="p-column-filter"
                  placeholder="Filtrer par date"
                />
              </template>
              <template #body="{ data }">
                {{ formatDateTimeString(data.date) }}
              </template>
            </p-column>
            <p-column field="subject" header="Sujet" sortable :showFilterMenu="false">
              <template #filter="{ filterModel, filterCallback }">
                  <InputText v-model="filterModel.value" type="text" @input="filterCallback()" class="p-column-filter" placeholder="Filtrer par sujet" />
              </template>
            </p-column>
            <p-column field="email" header="Destinataire" sortable :showFilterMenu="false">
              <template #body="{ data }">
                {{ data.email }}
              </template>
              <template #filter="{ filterModel, filterCallback }">
                <InputText
                  v-model="filterModel.value"
                  type="text"
                  @input="filterCallback()"
                  class="p-column-filter"
                  placeholder="Filtrer par destinataire"
                />
              </template>
            </p-column>
            <p-column field="status" header="Statut" sortable :showFilterMenu="false">
              <template #body="{ data }">
                <Tag :value="data.status" :severity="getSeverity(data.status)" rounded />
              </template>
              <template #filter="{ filterModel, filterCallback }">
                  <Dropdown v-model="filterModel.value" @change="filterCallback()" :options="statuses" placeholder="Sélectionnez" class="p-column-filter" style="min-width: 12rem" :showClear="true">
                      <template #option="slotProps">
                          <Tag :value="slotProps.option" :severity="getSeverity(slotProps.option)" rounded />
                      </template>
                  </Dropdown>
              </template>
            </p-column>
            <template #empty>Aucune donnée trouvée</template>
        </p-data-table>
      </section>
      <section v-else>Chargement en cours...</section>
    </main>
  </div>
</template>

<script setup lang="ts">
import PrimeVue from 'primevue/config';
import { ref, onBeforeMount } from 'vue'
import { getLogs } from '@/utils/appli_api'
import PDataTable from 'primevue/datatable'
import PColumn from 'primevue/column'
import { formatDateTimeString } from '@/utils/formatDate'
import { FilterService, FilterMatchMode, FilterOperator } from '@primevue/core/api';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import Dropdown from 'primevue/dropdown';


const loading = ref(false)
const errorStats = ref<string>('')
const logs = ref();
const status = ref();


async function refreshLogs() {
  loading.value = true
  errorStats.value = ''
  try {
    logs.value = await getLogs()
  } catch (error) {
    errorStats.value = error as string
  }
  loading.value = false
}
onBeforeMount(() => {
  refreshLogs()
})


const filters = ref();

FilterService.register('filterByDateFr', (value, filter) => {
  if (!filter) {
    return true;
  }
  return formatDateTimeString(value).includes(filter);
});

FilterService.register('filterByStatus', (value, filter) => {
  if (!filter) {
    return true;
  }
  return (value === filter)?true:false;
});

const initFilters = () => {
    filters.value = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        'date': { value: null, matchMode: "filterByDateFr" },
        'subject': { value: null, matchMode: FilterMatchMode.CONTAINS },
        'email': { value: null, matchMode: FilterMatchMode.CONTAINS },
        'status': { value: null, matchMode: "filterByStatus" },
    };
};

initFilters();

const clearFilter = () => {
  initFilters();
};

const statuses = ref(['connexion', 'rdv', 'confirmation', 'à confirmer', 'attente', 'annulation','info admin']);

const getSeverity = (status: string) => {
    switch (status) {
        case 'connexion':
            return 'secondary';
        case 'rdv':
            return 'info';
        case 'confirmation':
            return 'success';
        case 'à confirmer':
            return 'warn';
        case 'attente':
            return 'warn';
        case 'annulation':
            return 'danger';
        case 'info admin':
            return 'contrast';
        default:
            return undefined;
    }
};

</script>
