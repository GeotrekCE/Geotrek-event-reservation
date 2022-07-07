<template>
  <v-container name="event-search">
    <v-card>
      <v-card-title> Rechercher </v-card-title>
      <v-spacer></v-spacer>
      <v-form class="pa-md-4 mx-lg-auto" ref="form" @submit.prevent="search" lazy-validation>
        <v-row>
          <v-col cols="12" lg="12">
            <v-text-field v-model="filters.search_name" append-icon="mdi-magnify"
              label="Nom animation" single-line hide-details></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" lg="6">
            <date-picker label="Date de début" :dateValue.sync="filters.begin_date"
              @input="filters.begin_date = $event">
            </date-picker>
          </v-col>
          <v-col cols="12" lg="6">
            <date-picker label="Date de fin" :dateValue.sync="filters.end_date"
              @input="filters.end_date = $event">
            </date-picker>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" lg="4">
            <v-select multiple chips v-model="filters.massif" :items="districts" label="Massifs">
            </v-select>
          </v-col>
          <v-col cols="12" lg="4">
            <v-select multiple chips v-model="filters.type_id" :items="eventtypes" item-text="name"
              item-value="id" label="Type">
            </v-select>
          </v-col>
          <v-col cols="12" lg="2">
            <v-checkbox v-model="filters['published']" label="Publiées"></v-checkbox>
          </v-col>
          <v-col cols="12" lg="2">
            <v-checkbox v-model="filters['bilan.annulation']" label="Annulés"></v-checkbox>
          </v-col>
        </v-row>
        <v-row>
          <v-btn class="mr-4" type="submit" color="primary">
            Rechercher
          </v-btn>
          <v-btn @click="clear">
            Réinitialiser
          </v-btn>

        </v-row>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>

import { mapState, mapActions } from 'vuex';

import { getDistricts, getTouristiceventType } from '@/services/gta_api';
import DatePicker from './DatePicker.vue';

export default {
  components: { DatePicker },
  data() {
    return {
      filters: { },
      districts: [],
      eventtypes: []
    }
  },
  computed: {
    ...mapState({
      filtersState: (state) => state.events.filters
    })
  },
  mounted() {
    this.filters = this.filtersState;
    getDistricts().then(
      (data) => {
        this.districts = data.results.map((item) => item.name);
      }
    );
    getTouristiceventType().then(
      (data) => {
        this.eventtypes = data.results.map((item) => item.name);
      }
    );
  },
  methods: {
    ...mapActions(['saveFilters', '']),

    search() {
      this.saveFilters(this.filters);
      this.$emit('search', this.filters);
    },
    clear() {
      this.saveFilters(undefined);
      this.filters = this.filtersState;
      this.$emit('search', this.filters);
    },
  }
}
</script>

<style>

</style>
