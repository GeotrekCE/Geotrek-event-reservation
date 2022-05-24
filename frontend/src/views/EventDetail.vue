<template>
    <v-container name="event-list">
      <v-card class="mb-10" elevation="2" :loading="loading">
        <v-card-title :class="{ red: canceled }">
          {{event.name}}
          <span v-if="canceled === true"> - Annulé</span>
          <v-spacer></v-spacer>
          <event-cancel-form
            :bilan="event.bilan"
            :canceled="canceled"
            :id_event="id"
            v-on:reloadEvent="getEvent()"
          ></event-cancel-form>
        </v-card-title>
        <v-card-text>
          <div v-html='event.description_teaser'></div>
          <div v-if="event.type"><strong> Type : </strong> {{event.type.type}}</div>
          <div><strong> Massif : </strong> {{event.massif}}</div>
          <div><strong> Date début : </strong> {{event.begin_date}}</div>
          <div><strong> Info pratique (grand public) : </strong>
            <span v-html="event.practical_info_fr"></span>
          </div>
          <div><strong> Info pratique (privée) : </strong>
            <span v-html="event.practical_info_en"></span>
          </div>
          <div><strong> Public visé : </strong>
            <span v-html="event.target_audience"></span>
          </div>

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
    <v-tabs v-model="tab">
      <v-tab value="resa">Reservations</v-tab>
      <v-tab value="bilan">Bilan</v-tab>
    </v-tabs>
    <span v-if="tab == 0">
      <event-reservations
      :event="event"
      v-on:reloadEvent="getEvent()"
      :v-if="tab === 0"
      >
      </event-reservations>
    </span>
    <span v-if="tab == 1">
      <event-bilan
      :event="event"
      >
      </event-bilan>
    </span>
    </v-container>
</template>

<script>
import { mapGetters } from 'vuex';

import { config } from '@/config/config';
import { getOneEvent } from '@/services/appli_api'

import GtEventDetail from '@/components/GtEventDetail.vue'
import EventReservations from '@/components/EventReservations.vue'
import EventBilan from '@/components/EventBilan.vue'
import EventCancelForm from '@/components/EventCancelForm.vue'

export default {
  components: {
    GtEventDetail, EventReservations, EventCancelForm, EventBilan
  },
  data() {
    return {
      loading: true,
      id: parseInt(this.$route.params.id, 0),
      event: {},

      tab: 'resa',

      URL_GTR: config.URL_GTR,
      URL_GTA: config.URL_GTA
    };
  },
  computed: {
    ...mapGetters(['user']),
    canceled() {
      if (this.event.bilan) {
        return this.event.bilan.annulation;
      }
      return false;
    },
  },
  created() {
    this.getEvent();
  },
  mounted() {
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
  },
};
</script>
