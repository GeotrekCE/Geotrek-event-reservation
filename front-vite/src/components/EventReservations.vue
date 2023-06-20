<template>

  <p class="text-center my-4">
    <a
      class="text-blue-600 visited:text-purple-600"
      :href="lienExport + idEvent"
      target="_blank"
    >
      Exporter les données de réservation
    </a>
  </p>
  <p-data-table
    :value="resas.results"
    data-key="id_reservation"
    tableStyle="min-width: 50rem"
    stripedRows
    class="p-datatable-sm"
    lazy
    paginator
    scrollable
    :rows="10"
    :total-records="resas.total"
    :loading="loading"
    @page="emits('page', $event)"
    v-model:expandedRows="expandedRows"
  >
    <template #empty>Aucune réservation trouvée.</template>
    <template #loadingicon>
      <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
    </template>
    <p-column frozen expander />
    <p-column frozen field="nom" header="Nom"></p-column>
    <p-column field="prenom" header="Prénom"></p-column>
    <p-column field="email" header="email"></p-column>
    <p-column field="tel" header="Tél"></p-column>
    <p-column field="meta_create_date" header="Créée le">
      <template #body="{ data }">
        {{ formatDateTimeString(data.meta_create_date) }}
      </template>
    </p-column>
    <p-column header="Nombre d'inscrits">
      <template #body="{ data }">
        {{ data.liste_attente ? data.sum_participants_liste_attente : data.sum_participants }}
      </template>      
    </p-column>

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
    <!--
    <p-column field="confirmed" header="Confirmée">
      <template #body="{ data }">
        <p-tag
          class="rounded-sm"
          :value="data.confirmed ? 'Confirmée' : 'En attente'"
          :severity="data.confirmed ? 'success' : 'warning'"
        />
      </template>
    </p-column>
    <p-column field="cancelled" header="Annulée">
      <template #body="{ data }">
        <p-tag
          v-if="data.cancelled"
          class="rounded-sm"
          value="Annulée"
          severity="danger"
        />
      </template>
    </p-column>
    -->
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
        <div class="col-span-full mx-auto">
          <button
            @click="emits('confirm', data.id_reservation)"
            v-if="! data.confirmed"
            class="rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm bg-sky-600 hover:bg-sky-500"
          >Confirmer la réservation</button>

          <button
            @click="emits('edit', data.id_reservation)"
            class="rounded-sm ml-4 px-3 py-2 text-sm font-medium text-white shadow-sm bg-sky-600 hover:bg-sky-500"
          >Modifier la réservation</button>
        </div>
      </div>
    </template>
  </p-data-table>
</template>

<script setup lang="ts">
import PDataTable from 'primevue/datatable'
import PColumn from 'primevue/column'
import PTag from 'primevue/tag'
import { ref } from 'vue'
import { expandedFields } from '@/utils/fields'
import { formatDateTimeString } from '@/utils/formatDate'
import { useConfirm } from "primevue/useconfirm";

const confirm = useConfirm()

const lienExport = CONFIGURATION.URL_APPLICATION + '/export_reservation/'

defineProps({
  resas: {
    type: Object,
    required: false,
    default: () => ({
      results: [],
      total: 0
    })
  },
  loading: {
    type: Boolean,
    required: true
  },
  idEvent: {
    type: Number,
    required: true
  }
})
const emits = defineEmits(['page', 'cancel', 'confirm', 'edit'])

const expandedRows = ref([])

function onCancelResa(event: any, id_reservation: number) {
  confirm.require({
    target: event.currentTarget,
    message: 'Êtes vous sûr de vouloir annuler cette réservation ?',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Oui',
    rejectLabel: 'Non',
    accept: () => {
      emits('cancel', id_reservation)
    },
  })
}

/*
function addCalculateParticipant(): boolean {
  if (this.editedItem.liste_attente === true) return false;
  let nbInit = 0;

  // Si c'est une modification il faut soustraire le nombre de participants initial
  if (this.editedItem.id_reservation !== undefined) {
    const resa = this.event.reservations.filter(
      (item: Resa) => item.id_reservation === this.editedItem.id_reservation
    )[0];
    nbInit = Object.keys(
      this.liste_champs_nb
    ).reduce(
      (total, nb) => (
        total + (parseInt(resa[nb], 0) || 0)
      ), 0
    )
  }
  const sumP: number = (Object.keys(this.liste_champs_nb) as Array<keyof Resa>)
  .reduce(
    (total, nb) => (
      total + (parseInt(this.editedItem[nb] as string, 0) || 0)
    ), 0
  ) + this.event.sum_participants - nbInit;

  // Faux si la sum des participant est supérieur au nb de place + delta défini dans la CONFIGURATION
  return sumP > parseInt(this.event.capacity, 0) + CONFIGURATION.RESA_NB_DELTA
}
*/
</script>
