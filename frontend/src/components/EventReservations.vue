<template>
    <v-container name="event-list">

    <v-data-table
      :headers="headers"
      :items="event.reservations"
      sort-by="nb"
      class="elevation-1"
      :v-if="loading"
    >
    <template v-slot:top >
      <v-toolbar
        flat
      >
        <reservation-progress
          :reservation-nb="event.sum_participants"
          :participant-nb="event.participant_number"
          :attente-nb="event.sum_participants_liste_attente"
          style="width=25%"
        >
        </reservation-progress>
        <v-divider class="mx-4" inset vertical ></v-divider>
        <v-spacer></v-spacer>
        <v-dialog
          v-model="dialog"

        >
          <template v-slot:activator="{ editedItem }">
             <v-btn
              color="primary"
              dark
              class="mb-2"
              v-bind="editedItem"
              @click="addItem"
              v-show="reservationOpened"
              key="res_open"
            >
              Nouvelle réservation
            </v-btn>
            <div
              v-show="!reservationOpened" >
             <span
              class="grey lighten-2 text-center px-2">
              Réservation non ouverte
            </span>
            </div>
          </template>
          <v-card>
            <v-card-title>
                <span class="text-h5">{{ formTitle }}
                <reservation-progress
                :reservation-nb="event.sum_participants"
                :participant-nb="event.participant_number"
                :attente-nb="event.sum_participants_liste_attente"
                >
                </reservation-progress></span>
            </v-card-title>
            <v-card-text>
              <v-container name="reservation-form">
                <v-alert
                text
                dense
                icon="mdi-information-outline"
                border="left"
              >
              <strong> Public visé : </strong><span v-html="event.target_audience"></span>
              </v-alert>
                <v-form
                  ref="reservation_form"
                  v-model="valid"
                  lazy-validation
                >
              <v-expansion-panels
                v-model="openPanels"
                multiple
                >
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
                          <v-text-field v-model="editedItem.tel" label="Téléphone">
                          </v-text-field>
                        </v-col>
                      <v-col cols="12" sm="12" md="6">
                        <v-text-field v-model="editedItem.num_departement" label="Département">
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
                   <v-alert
                    :value="true"
                    type="error"
                    width="100%"
                    v-if="addCalculateParticipant"
                  >
                    Trop de participants
                  </v-alert>
                </v-row>
                <v-row>
                   <v-checkbox
                      v-model="editedItem.liste_attente"
                      label="Liste attente"
                    ></v-checkbox>
                </v-row>
                <v-row>
                  <v-col cols="12" sm="6" md="6" v-for="(field, index) in liste_champs_nb"
                  :key="index">
                    <v-text-field v-model="editedItem[field]"
                      min="0"
                      :rules="[rules.integer]"
                      :label="field">
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
                    <v-text-field
                      outlined
                      v-model="editedItem.commentaire_numerisateur"
                      label="Numérisation"
                    >
                    </v-text-field>
                </v-row>
                <v-row>
                    <v-textarea outlined v-model="editedItem.commentaire" label="Commentaire">
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
        <v-simple-checkbox
          v-model="item.liste_attente"
          disabled
        ></v-simple-checkbox>
      </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
      <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
    </template>
  </v-data-table>
    </v-container>
</template>

<script>
import { mapGetters } from 'vuex';

import { config } from '@/config/config';
import { deleteOneReservation, postOneReservation } from '@/services/appli_api'

import ReservationProgress from '@/components/ReservationProgress.vue';

export default {
  components: { ReservationProgress },
  props: ['event'],
  data() {
    return {
      openPanels: [0, 1, 2],
      valid: false,
      rules: {
        required: (value) => !!value || 'Champ obligatoire.',
        integer: (value) => (!Number.isNaN(Number(value)) && value !== '') || 'Uniquement des chiffres',
        email: (value) => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Invalid e-mail.'
        },
      },
      liste_champs_nb: ['nb_adultes', 'nb_moins_6_ans', 'nb_6_8_ans', 'nb_9_12_ans', 'nb_plus_12_ans'],
      userMgstext: '',
      loading: true,
      id: parseInt(this.$route.params.id, 0),
      dialog: false,
      dialogDelete: false,
      headers: [
        { text: 'nom', value: 'nom' },
        { text: 'prenom', value: 'prenom' },
        { text: 'tel', value: 'tel' },
        { text: 'total', value: 'sum_participants' },
        { text: 'total_attente', value: 'sum_participants_liste_attente' },
        { text: 'nb_adultes', value: 'nb_adultes' },
        { text: 'nb_moins_6_ans', value: 'nb_moins_6_ans' },
        { text: 'nb_6_8_ans', value: 'nb_6_8_ans' },
        { text: 'nb_9_12_ans', value: 'nb_9_12_ans' },
        { text: 'nb_plus_12_ans', value: 'nb_plus_12_ans' },
        { text: 'num_departement', value: 'num_departement' },
        { text: 'liste_attente', value: 'liste_attente' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      editedItem: {},
      numerisateurName: undefined,
      URL_GTR: config.URL_GTR,
      URL_GTA: config.URL_GTA
    };
  },
  computed: {
    ...mapGetters(['user']),

    reservationOpened() {
      // Define if reservation is open

      // If event is happened
      if (new Date() >= new Date(this.event.begin_date)) {
        return false
      }

      // If event in reservation period (control by DAY_BEFORE_RESA)
      if ((config.DAY_BEFORE_RESA || -1) !== -1) {
        const resaBeginDate = new Date(this.event.begin_date);
        resaBeginDate.setDate(resaBeginDate.getDate() - config.DAY_BEFORE_RESA);
        if (new Date() >= resaBeginDate) {
          return true;
        }
        return false;
      }

      return true;
    },
    defaultItem() {
      const fieldsnb = this.liste_champs_nb.reduce((o, key) => ({ ...o, [key]: 0 }), {})
      return {
        ...{
          nom: '',
          prenom: '',
          commentaire: '',
          event: this.$route.params.id,
          liste_attente: false,
          id_numerisateur: this.user.id_role
        },
        ...fieldsnb
      }
    },
    formTitle() {
      return this.editedItem.id_reservation === undefined ? 'Nouvelle réservation' : 'Editer réservation'
    },
    addCalculateParticipant() {
      if (this.editedItem.liste_attente === true) return false;
      let nbInit = 0;

      // Si c'est une modification il faut soustraire le nombre de participants initial
      if (this.editedItem.id_reservation !== undefined) {
        const resa = this.event.reservations.filter(
          (item) => item.id_reservation === this.editedItem.id_reservation
        )[0];
        nbInit = this.liste_champs_nb.reduce(
          (total, nb) => (
            total + (parseInt(resa[nb], 0) || 0)
          ), 0
        )
      }
      const sumP = this.liste_champs_nb.reduce(
        (total, nb) => (
          total + (parseInt(this.editedItem[nb], 0) || 0)
        ), 0
      ) + this.event.sum_participants - nbInit;

      // Faux si la sum des participant est supérieur au nb de place + delta défini dans la config
      return sumP > parseInt(this.event.participant_number, 0) + config.RESA_NB_DELTA
    },
  },
  watch: {
    dialog(val) {
      return val || this.close()
    },
    dialogDelete(val) {
      return val || this.closeDelete()
    },
  },
  created() {
  },
  mounted() {
    setTimeout(() => {
      if (this.$refs.reservation_form) {
        (this.$refs.reservation_form).validate();
      }
    }, 2000);
  },
  methods: {
    addItem() {
      this.editedItem = { ...this.defaultItem };
      this.numerisateurName = undefined;
      this.dialog = true;
    },

    editItem(item) {
      this.editedItem = { ...item };
      this.numerisateurName = item.numerisateur
        ? item.numerisateur.identifiant
        : undefined;

      this.editedItem.id_numerisateur = this.user.id_role;
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedItem = item;
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      deleteOneReservation(this.editedItem.id_reservation).then((data) => {
        this.getEvent();
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

      postOneReservation(this.editedItem).then((data) => {
        this.$emit('reloadEvent');
      })
      this.close()
    },
  },
};
</script>
