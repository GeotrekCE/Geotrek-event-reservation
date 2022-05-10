<template>
    <v-container name="event-list">
      <v-card class="mb-10" elevation="2" :loading="loading">
        <v-card-title>
        {{event.name}}
        </v-card-title>
        <v-card-subtitle  v-html='event.description_teaser'></v-card-subtitle>
        <v-card-text>
          <div v-if="event.type"><strong> Type : </strong> {{event.type.type}}</div>
          <div><strong> Massif : </strong> {{event.massif}}</div>
          <div><strong> Date début : </strong> {{event.begin_date}}</div>
          <div><strong> Date fin : </strong> {{event.end_date}}</div>
            <div class="text-center">
              <v-btn
                :href="URL_GTR + '/event/' + event.id"
                target="_blank"
                class="mr-2"
                color="cyan"
                :disabled="event.published !== true"
              >
                <v-icon>mdi-open-in-new</v-icon> Destination cévennes
              </v-btn>
              <v-btn
                :href="URL_GTA + '/touristicevent/' + event.id"
                target="_blank"
                color="light-green lighten-1"
              >
                <v-icon>mdi-open-in-new</v-icon> Geotrek admin
              </v-btn>
            </div>
        </v-card-text>
      </v-card>
    <div
      v-if="event.published === true"
    >
      <gt-event-detail class="mb-10" :id="id" :published="event.published"></gt-event-detail>
    </div>
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
        <v-toolbar-title>Réservations
          <reservation-progress
            :reservation-nb="event.sum_participants"
            :participant-nb="event.participant_number"
            :attente-nb="event.sum_participants_liste_attente"
          >
          </reservation-progress>
        </v-toolbar-title>
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
              </reservation-progress>
          </span>
            </v-card-title>
            <v-card-text>
              <v-container name="reservation-form">
                <v-form
                  ref="reservation_form"
                  v-model="valid"
                  lazy-validation
                >
                <v-row>
                   <v-checkbox
                      v-model="editedItem.liste_attente"
                      label="Liste attente"
                    ></v-checkbox>
                </v-row>
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
                      <v-text-field v-model="editedItem.tel" label="Téléphone"></v-text-field>
                    </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field v-model="editedItem.num_departement" label="Département">
                    </v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                    <v-textarea outlined v-model="editedItem.contact" label="Contact"></v-textarea>
                </v-row>
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
                  <v-col cols="12" sm="6" md="6" v-for="(field, index) in liste_champs_nb"
                  :key="index">
                    <v-text-field v-model="editedItem[field]"
                      min="0"
                      :rules="[rules.integer]"
                      :label="field">
                    </v-text-field>
                  </v-col>
                </v-row>
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

    <v-snackbar
      v-model="openSnackbar"
      color="success"
    >
      {{ userMgstext }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="openSnackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    </v-container>
</template>

<script>
import { config } from '@/config/config';
import { getOneEvent, deleteOneReservation, postOneReservation } from '@/services/appli_api'

import GtEventDetail from '@/components/GtEventDetail.vue'
import ReservationProgress from '@/components/ReservationProgress.vue';

export default {
  components: { GtEventDetail, ReservationProgress },
  data() {
    return {
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
      openSnackbar: false,
      userMgstext: '',
      loading: true,
      id: parseInt(this.$route.params.id, 0),
      event: {},
      dialog: false,
      dialogDelete: false,
      headers: [
        { text: 'nom', value: 'nom' },
        { text: 'prenom', value: 'prenom' },
        { text: 'tel', value: 'tel' },
        { text: 'contact', value: 'contact' },
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
      URL_GTR: config.URL_GTR,
      URL_GTA: config.URL_GTA
    };
  },
  computed: {
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
          contact: '',
          event: this.$route.params.id,
          liste_attente: false
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
    this.getEvent();
  },
  mounted() {
    setTimeout(() => {
      if (this.$refs.reservation_form) {
        (this.$refs.reservation_form).validate();
      }
    }, 2000);
  },
  methods: {
    getEvent() {
      getOneEvent(this.id).then((data) => {
        this.event = data;
        this.loading = false;
      }).catch((error) => {
        this.errorMessage = error;
        console.error('There was an error!', error);
      });
    },

    addItem() {
      this.editedItem = { ...this.defaultItem };
      this.dialog = true;
    },

    editItem(item) {
      this.editedItem = { ...item };
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedItem = item;
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      deleteOneReservation(this.editedItem.id_reservation).then((data) => {
        this.userMgstext = 'Donnée supprimée';
        this.openSnackbar = true;
        this.getEvent();
      }).catch((error) => {
        console.error('There was an error!', error);
        this.userMgstext = 'Erreur dans la suppression';
        this.openSnackbar = true;
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
      postOneReservation(this.editedItem).then((data) => {
        this.userMgstext = 'Données sauvegardées';
        this.openSnackbar = true;
        this.getEvent();
      }).catch((error) => {
        console.error('There was an error!', error);
        this.userMgstext = 'Erreur dans la sauvegarde';
        this.openSnackbar = true;
      });
      this.close()
    },
  },
};
</script>
