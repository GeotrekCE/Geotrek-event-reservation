<template>
  <v-expansion-panels
      :v-model="[0]">
    <v-expansion-panel>
      <v-expansion-panel-header
      color="light-green lighten-1">
         <h2>Détail animation</h2>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <div v-if="gtevent">
          <div v-for="(field, index) in apiFields" :key="index">
          <b>{{field.label}} </b>: <span v-html="getFieldValue(index)"></span>
          <v-divider></v-divider>
          </div>
        </div>
        </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script lang="ts">

import { getTouristicEventDetail } from '@/utils/gta_api';

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
        capacity: { label: 'Nb participants' },
        'practical_info.fr': { label: 'Info pratique publique' },
        'practical_info.en': { label: 'Info pratique privé' },
        speaker: { label: 'Intervenant' },
        target_audience: { label: 'Public visé' },
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
    getFieldValue(field: any) {
      return field.split('.').reduce(
        (subevent: any, c: string) => ((c in subevent) ? subevent[c] : subevent),
        this.gtevent
      );
    }
  },
  async created() {
    if (this.published) {
      try {
        this.gtevent = await getTouristicEventDetail(this.id)
      } catch {
        this.gtevent = undefined;
      }
    }
  }
}
</script>