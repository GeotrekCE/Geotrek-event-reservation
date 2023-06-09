<template>
  <div name="event-reservation-list">
    {{ event.reservations }}
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
              <v-card-title>
                <span class="text-h5">{{ formTitle }} - {{ event.name }}
                </span>
                <reservation-progress :reservation-nb="event.sum_participants"
                  :participant-nb="event.capacity"
                  :attente-nb="event.sum_participants_liste_attente">
                </reservation-progress>
              </v-card-title>
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
                          Informations personnelles
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                          <v-row>
                            <v-col cols="12" sm="12" md="6">
                              <v-text-field v-model="editedItem.nom" label="Nom"
                                :rules="[rules.required]"></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="12" md="6">
                              <v-text-field v-model="editedItem.prenom" label="Prénom"
                                :rules="[rules.required]"></v-text-field>
                            </v-col>
                          </v-row>
                          <v-row>
                            <v-col cols="12" sm="12" md="6">
                              <v-text-field v-model="editedItem.tel" label="Téléphone"
                                :rules="[rules.required]">
                              </v-text-field>
                            </v-col>
                            <v-col cols="12" sm="12" md="6">
                              <v-text-field v-model="editedItem.num_departement" label="Département"
                                :rules="[rules.required]">
                              </v-text-field>
                            </v-col>
                          </v-row>
                        </v-expansion-panel-content>
                      </v-expansion-panel>
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
  </div>
</template>

<script lang="ts">
import { fieldsClasseAge, rulesFct } from '@/utils/fields'
// import { VDataTable } from 'vuetify/labs/VDataTable'

import { deleteOneReservation, postOneReservation } from '@/utils/appli_api'
import type { Resa, ResaEventFilters } from '@/declaration';

// import ReservationProgress from '@/components/ReservationProgress.vue';

export default {
  // components: { ReservationProgress, VDataTable },
  props: ['event', 'user'],
  data() {
    return {
      openPanels: [0, 1, 2],
      valid: false,
      userMgstext: '',
      loading: true,
      id: parseInt(this.$route.params.id as string, 0),
      dialog: false,
      dialogDelete: false,
      expanded: [],
      URL_APPLICATION: CONFIGURATION.URL_APPLICATION,
      headers: [
        { text: 'nom', value: 'nom' },
        { text: 'prenom', value: 'prenom' },
        { text: 'total', value: 'sum_participants' },
        { text: 'total_attente', value: 'sum_participants_liste_attente' },
        { text: 'nb_adultes', value: 'nb_adultes' },
        { text: 'nb_moins_6_ans', value: 'nb_moins_6_ans' },
        { text: 'nb_6_8_ans', value: 'nb_6_8_ans' },
        { text: 'nb_9_12_ans', value: 'nb_9_12_ans' },
        { text: 'nb_plus_12_ans', value: 'nb_plus_12_ans' },
        { text: 'liste_attente', value: 'liste_attente' },
        { text: 'Actions', value: 'actions', sortable: false },
        { text: '', value: 'data-table-expand' },
      ],
      editedItem: {} as Partial<Resa>,
      numerisateurName: undefined as string | undefined,
      URL_GTR: CONFIGURATION.URL_GTR,
      URL_GTA: CONFIGURATION.URL_GTA
    };
  },
  computed: {

    liste_champs_nb() {
      return fieldsClasseAge;
    },
    rules() {
      return rulesFct;
    },
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
  mounted() {
    this.validateForm()
  },
  methods: {
    addItem() {
      this.editedItem = { ...this.defaultItem };
      this.numerisateurName = undefined;
      this.dialog = true;
      this.validateForm()
    },

    editItem(item: Resa) {
      this.editedItem = { ...item };
      this.numerisateurName = item.numerisateur
        ? item.numerisateur.identifiant
        : undefined;
      this.dialog = true;
      this.validateForm()
    },

    deleteItem(item: Resa) {
      this.editedItem = item;
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      deleteOneReservation(this.editedItem.id_reservation).then(() => {
        this.$emit('reloadEvent');
      }).catch((error) => {
        console.error('There was an error!', error);
      });
      this.closeDelete()
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = this.defaultItem;
      })
    },

    closeDelete() {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = this.defaultItem;
      })
    },

    save() {
      // Set digitizer
      this.editedItem.id_numerisateur = this.user.id_role;
      postOneReservation(this.editedItem).then(() => {
        this.$emit('reloadEvent');
      })
      this.close()
    },

    validateForm() {
      setTimeout(() => {
        // @ts-expect-error
        this.$refs.reservation_form?.validate();
      }, 500);
    }
  },
  watch: {
    dialog(val) {
      return val || this.close()
    },
    dialogDelete(val) {
      return val || this.closeDelete()
    },
  },
};
</script>
