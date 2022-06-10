<template>
  <v-container name="event-list">
    <v-card class="mb-10" elevation="2" :loading="loading">
      <v-card-title>
        {{ event.name }}
        <v-spacer></v-spacer>
        <event-cancel-form :bilan="event.bilan" :canceled="canceled" :id_event="id"
          v-on:reloadEvent="getEvent()"></event-cancel-form>
      </v-card-title>
      <v-card-text>
        <v-alert v-if="canceled === true" dense outlined type="error">
          <h2>Animation annulée</h2>
          <div>
            <strong> Raison: </strong>
            <span>{{ event.bilan.raison_annulation }}</span>
          </div>
        </v-alert>

        <div v-html='event.description_teaser'></div>
        <div v-if="event.type"><strong> Type : </strong> {{ event.type.type }}</div>
        <div><strong> Massif : </strong> {{ event.massif }}</div>
        <div><strong> Date début : </strong> {{ event.begin_date }}</div>
        <div v-if="event.published === true && gtevent">
          <div v-for="(field, index) in getGtFields(true)" :key="index">
            <strong>{{ field.label }} : </strong>
            <span v-html="getGtFieldValue(index)"></span>
          </div>
          <v-btn v-on:click="showMore = !showMore">Plus d'informations
            <v-icon v-if="showMore">mdi-chevron-down</v-icon>
            <v-icon v-if="!showMore">mdi-chevron-right</v-icon>
          </v-btn>
          <span v-if="showMore">
            <div v-for="(field, index) in getGtFields(false)" :key="index">
              <strong>{{ field.label }} : </strong>
              <span v-html="getGtFieldValue(index)"></span>
            </div>
          </span>
        </div>
        <div class="text-center">
          <v-btn :href="URL_GTR + '/event/' + event.id" target="_blank" class="mr-2" color="cyan"
            :disabled="event.published !== true">
            <v-icon>mdi-open-in-new</v-icon> Destination cévennes
          </v-btn>
          <v-btn :href="URL_GTA + '/touristicevent/' + event.id" target="_blank"
            color="light-green lighten-1">
            <v-icon>mdi-open-in-new</v-icon> Geotrek admin
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    <!-- <div v-if="event.published === true">
      <gt-event-detail class="mb-10" :id="id" :published="event.published"></gt-event-detail>
    </div> -->
    <v-tabs v-model="tab">
      <v-tab value="resa">Reservations</v-tab>
      <v-tab value="bilan">Bilan</v-tab>
    </v-tabs>
    <span v-if="tab == 0">
      <event-reservations :event="event" v-on:reloadEvent="getEvent()" :v-if="tab === 0">
      </event-reservations>
    </span>
    <span v-if="tab == 1">
      <event-bilan v-if="!canceled" :event="event" v-on:reloadEvent="getEvent()">
      </event-bilan>
      <div v-else>
        <v-alert text dense icon="mdi-information-outline" border="left">
          L'animation a été annulée, il n'y a pas de bilan à saisir
        </v-alert>
      </div>
    </span>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';

import { config } from '@/config/config';
import { getOneEvent } from '@/services/appli_api'
import { getTouristicEventDetail } from '@/services/gta_api';
import { gtApiFields } from '@/utils/fields'

// import GtEventDetail from '@/components/GtEventDetail.vue'
import EventReservations from '@/components/EventReservations.vue'
import EventBilan from '@/components/EventBilan.vue'
import EventCancelForm from '@/components/EventCancelForm.vue'

export default {
  components: {
    // GtEventDetail,
    EventReservations, EventCancelForm, EventBilan
  },
  data() {
    return {
      loading: true,
      id: parseInt(this.$route.params.id, 0),
      event: {},
      gtevent: undefined,
      showMore: false,
      tab: 'resa',
      gtfields: gtApiFields,
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
    getGtFields(main) {
      return Object.keys(this.gtfields)
        .filter((key) => this.gtfields[key].main === main)
        .reduce((res, key) => ({ ...res, [key]: this.gtfields[key] }), {});
    },
    getGtFieldValue(field) {
      return field.split('.').reduce(
        (subevent, c) => ((c in subevent) ? subevent[c] : subevent),
        this.gtevent
      );
    },
    getEvent() {
      getOneEvent(this.id).then((data) => {
        this.event = data;
        if (this.event.published) {
          getTouristicEventDetail(this.id).then(
            (gtdata) => {
              this.gtevent = gtdata;
              this.loading = false;
            }
          ).catch((error) => {
            this.gtevent = undefined;
            this.loading = false;
          });
        } else {
          this.loading = false;
        }
      }).catch((error) => {
        this.errorMessage = error;
        console.error('There was an error!', error);
      });
    },
  },
};
</script>
