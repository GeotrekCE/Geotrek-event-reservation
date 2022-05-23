<template>
  <v-expansion-panels
      :v-model="[0]">
    <v-expansion-panel>
      <v-expansion-panel-header
      color="light-green lighten-1">
         <h2>Détail animation</h2>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <div v-if="this.gtevent">
          <div v-for="(field, index) in apiFields" :key="index">
          <b>{{field.label}} </b>: <span v-html="getFieldValue(index)"></span>
          <v-divider></v-divider>
          </div>
        </div>
        </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>

import { getTouristicEventDetail } from '@/services/gta_api';

export default {
  data() {
    return {
      gtevent: undefined,
      apiFields: {
        booking: { label: 'Reservation' },
        contact: { label: 'Contact' },
        'name.fr': { label: 'Nom' },
        'description_teaser.fr': { label: 'Description courte', type: 'html' },
        'description.fr': { label: 'Description', type: 'html' },
        duration: { label: 'Durée' },
        email: { label: 'Email' },
        begin_date: { label: 'Date début' },
        end_date: { label: 'Date fin' },
        meeting_point: { label: 'Lieu de RDV' },
        meeting_time: { label: 'Heure de RDV' },
        organizer: { label: 'Organisateur' },
        participant_number: { label: 'Nb participants' },
        'practical_info.fr': { label: 'Info pratique publique' },
        'practical_info.en': { label: 'Info pratique privé' },
        speaker: { label: 'Intervenant' },
        target_audience: { label: 'Cible' },
      }
    }
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
    published: {
      type: Boolean
    },
  },
  computed: {
  },
  methods: {
    getFieldValue(field) {
      return field.split('.').reduce(
        (subevent, c) => ((c in subevent) ? subevent[c] : subevent),
        this.gtevent
      );
    }
  },
  created() {
    if (this.published) {
      getTouristicEventDetail(this.id).then(
        (data) => {
          this.gtevent = data;
        }
      ).catch((error) => {
        this.gtevent = undefined;
      });
    }
  }
}
</script>

<style>

</style>
