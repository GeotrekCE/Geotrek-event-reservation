<template>
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
        {{ formatDateTime(data.meta_create_date) }}
      </template>
    </p-column>
    <p-column field="sum_participants" header="Total"></p-column>
    <p-column field="sum_participants_liste_attente" header="Liste d'attente"></p-column>
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
          class="rounded-sm"
          :value="data.cancelled ? 'Annulée' : ''"
          :severity="data.cancelled ? 'danger' : 'success'"
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
        <div class="col-span-full mx-auto">
          <button
            @click="emits('confirm', data.id_reservation)"
            v-if="! data.confirmed"
            class="rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm bg-sky-600 hover:bg-sky-500"
          >Confirmer la réservation</button>
        </div>
      </div>
    </template>
  </p-data-table>

  <!-- <div name="event-reservation-list"> -->
    <!-- <v-data-table :headers="headers" :items="event.reservations" v-model:expanded="expanded"
      show-expand item-key="id_reservation" sort-by="nb" class="elevation-1" :v-if="loading">
      <template v-slot:top>
        <v-toolbar flat>
          <reservation-progress :reservation-nb="event.sum_participants"
            :participant-nb="event.capacity"
            :attente-nb="event.sum_participants_liste_attente" style="width=25%">
          </reservation-progress>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog">
            <template v-slot:activator="{ editedItem }">
              <v-btn color="primary" dark class="mb-2" v-bind="editedItem" @click="addItem"
                v-show="reservationOpened" key="res_open">
                Nouvelle réservation
              </v-btn>
              <div v-show="!reservationOpened">
                <span class="grey lighten-2 text-center px-2">
                  Réservation non ouverte
                </span>
              </div>
            </template>
            <v-card>
              <v-card-text>
                <v-container name="reservation-form">
                  <v-alert text dense icon="mdi-information-outline" border="left">
                    <div><strong> Public visé : </strong><span
                        v-html="event.target_audience"></span></div>
                    <div v-if="numerisateurName">
                      <strong> Réservation réalisée par :</strong><span>{{numerisateurName}}</span>
                    </div>
                  </v-alert>
                  <v-form ref="reservation_form" v-model="valid" lazy-validation>
                    <v-expansion-panels v-model="openPanels" multiple>
                      <v-expansion-panel>
                        <v-expansion-panel-header>
                          Nombres participants
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                          <v-row>
                            <v-alert :value="true" type="error" width="100%"
                              v-if="addCalculateParticipant">
                              Trop de participants
                            </v-alert>
                          </v-row>
                          <v-row>
                            <v-checkbox v-model="editedItem.liste_attente" label="Liste attente">
                            </v-checkbox>
                          </v-row>
                          <v-row>
                            <v-col cols="12" sm="6" md="6" v-for="(field, index) in liste_champs_nb"
                              :key="index">
                              <v-text-field v-model="editedItem[index]" min="0"
                                :rules="[rules.integer]" :label="field">
                              </v-text-field>
                            </v-col>
                          </v-row>
                        </v-expansion-panel-content>
                      </v-expansion-panel>
                      <v-expansion-panel>
                        <v-expansion-panel-header>
                          Autre
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                          <v-row>
                            <v-text-field outlined v-model="editedItem.commentaire_numerisateur"
                              :rules="[rules.required]"
                              label="Nom personne ayant réalisée l'inscription">
                            </v-text-field>
                          </v-row>
                          <v-row>
                            <v-textarea outlined v-model="editedItem.commentaire"
                              label="Commentaire">
                            </v-textarea>
                          </v-row>
                        </v-expansion-panel-content>
                      </v-expansion-panel>
                    </v-expansion-panels>
                  </v-form>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">
                  Annuler
                </v-btn>
                <v-btn color="blue darken-1" text @click="save"
                  :disabled="!valid || addCalculateParticipant">
                  Enregistrer
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5">
                Etes vous sur de supprimer cette réservation
              </v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.liste_attente="{ item }">
        <v-simple-checkbox v-model="item.liste_attente" disabled></v-simple-checkbox>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
        <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <div><strong> Téléphone : </strong> {{ item.tel }}</div>
          <div><strong> Département : </strong> {{ item.num_departement }}</div>
          <div><strong> Commentaire : </strong> {{ item.commentaire }}</div>
          <div><strong> Numérisateur : </strong>
            <span v-if="item.numerisateur">{{ item.numerisateur.identifiant }} - </span>
            {{item.commentaire_numerisateur }}
          </div>
          <div><strong> Enregistré le : </strong> {{ item.meta_create_date }}
            <span v-if="item.meta_update_date">
              <strong> Modifié le : </strong> {{ item.meta_update_date }}
            </span>
          </div>
        </td>
      </template>
      <template v-slot:footer.page-text>
        <v-btn color="primary" dark class="ma-2"
          :href=" URL_APPLICATION + '/export_reservation/' + id" target="_blank">
          Exporter
        </v-btn>
      </template>
    </v-data-table> -->
  <!-- </div> -->
</template>

<script setup lang="ts">
import PDataTable from 'primevue/datatable'
import PColumn from 'primevue/column'
import PTag from 'primevue/tag'
import { ref } from 'vue'
import { expandedFields } from '@/utils/fields'
import { formatDateTime } from '@/utils/formatDate'
import { useConfirm } from "primevue/useconfirm";

const confirm = useConfirm()

defineProps({
  resas: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    required: true
  }
})
const emits = defineEmits(['page', 'cancel', 'confirm'])

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


// import { deleteReservation, postReservation } from '@/utils/appli_api'
// import type { Resa, ResaEventFilters } from '@/declaration';

// import ReservationProgress from '@/components/ReservationProgress.vue';
/*
export default {
  computed: {

    reservationOpened() {
      // Define if reservation is open

      // If event is happened

      if (new Date().setHours(0, 0, 0, 0) > new Date(this.event.begin_date).setHours(0, 0, 0, 0)) {
        return false
      }

      // If event in reservation period (control by DAY_BEFORE_RESA)
      if ((CONFIGURATION.DAY_BEFORE_RESA || -1) !== -1) {
        const resaBeginDate = new Date(this.event.begin_date);
        resaBeginDate.setDate(resaBeginDate.getDate() - CONFIGURATION.DAY_BEFORE_RESA);
        if (new Date().setHours(0, 0, 0, 0) >= resaBeginDate.setHours(0, 0, 0, 0)) {
          return true;
        }
        return false;
      }

      return true;
    },
    defaultItem(): Partial<Resa> {
      const fieldsnb = Object.keys(
        this.liste_champs_nb
      ).reduce((o, key) => ({ ...o, [key]: 0 }), {});
      return {
        ...{
          nom: '',
          prenom: '',
          commentaire: '',
          id_event: parseInt(this.$route.params.id as string, 10)
        },
        ...fieldsnb
      }
    },
    formTitle(): string {
      return this.editedItem.id_reservation === undefined ? 'Nouvelle réservation' : 'Editer réservation'
    },
    addCalculateParticipant(): boolean {
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
    },
  },
  },
};
*/
</script>
