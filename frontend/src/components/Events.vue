<template>
  <div name="event-detail">
    <h1 style="text-align: center;">Animations du Parc national des Cévennes</h1>
    <v-container  name="event-search">
      <v-card>
        <v-card-title> Rechercher </v-card-title>
        <v-spacer></v-spacer>
        <v-form  class="pa-md-4 mx-lg-auto"
            ref="form"
            @submit.prevent="search"
            lazy-validation
          >
          <v-row>
            <v-col cols="12" lg="12">
              <v-text-field
                v-model="filters.search_name"
                append-icon="mdi-magnify"
                label="Nom animations"
                single-line
                hide-details
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" lg="6">
            <date-picker label="Date de début" :dateValue="filters.begin_date"
              @input="filters.begin_date=$event"></date-picker>
            </v-col>
            <v-col cols="12" lg="6">
            <date-picker label="Date de fin" :dateValue="filters.end_date"
              @input="filters.end_date=$event"></date-picker>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" lg="6">
              <v-select
                v-model="filters.massif"
                :items="districts"
                label="Massifs"
              ></v-select>
            </v-col>
            <v-col cols="12" lg="6">
              <v-select
                v-model="filters.type_id"
                :items="eventtypes"
                item-text="name"
                item-value="id"
                label="Type"
              ></v-select>
            </v-col>
          </v-row>
            <v-row>
              <v-btn
              class="mr-4"
              type="submit"
              color="primary"
            >
              Rechercher
            </v-btn>
            <v-btn @click="clear">
              Réinitialiser
            </v-btn>

            </v-row>
        </v-form>
      </v-card>
    </v-container>
    <v-data-table
      :page="page"
      :pageCount="numberOfPages"
      :headers="headers"
      :items="events"
      :options.sync="options"
      :server-items-length="totalEvents"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.id="{ item }">
        <router-link :to="{ name: 'event', params: { id: item.id }}">
          <v-btn icon color="pink"  >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </router-link>
      </template>
      <template v-slot:item.remplissage="{ item }">

          <reservation-progress
            :reservation-nb="item.sum_participants"
            :participant-nb="item.participant_number"
            :attente-nb="item.sum_participants_liste_attente"
          >
          </reservation-progress>

      </template>

    </v-data-table>
  </div>
</template>

<script>
import { getEvents } from '@/services/appli_api';
import { getDistricts, getTouristiceventType } from '@/services/gta_api';
import DatePicker from './subcomponents/DatePicker.vue';
import ReservationProgress from './subcomponents/ReservationProgress.vue';

export default {
  components: { DatePicker, ReservationProgress },
  name: 'DatatableComponent',
  data() {
    return {
      power: 78,
      page: 1,
      totalEvents: 0,
      numberOfPages: 0,
      events: [],
      loading: true,
      options: {},
      filters: {
        begin_date: undefined,
        end_date: undefined,
        search_name: undefined,
      },
      headers: [
        { text: 'Remplissage', value: 'remplissage' },
        { text: 'Nom', value: 'name' },
        { text: 'Date début', value: 'begin_date' },
        { text: 'Date fin', value: 'end_date' },
        { text: 'Type', value: 'type.type' },
        { text: 'Massif', value: 'massif' },
        { text: 'Attente', value: 'sum_participants_liste_attente' },
        { text: 'id', value: 'id' },
      ],
      districts: [],
      eventtypes: []
    };
  },
  watch: {
    options: {
      handler() {
        this.getEvents();
      },
    },
    deep: true,
  },
  computed: {
  },
  methods: {
    clear() {
      this.filters = {
        begin_date: undefined,
        end_date: undefined,
        search_name: undefined,
      }
    },
    search() {
      this.options.page = 1;
      this.getEvents();
    },
    getEvents() {
      this.loading = true;
      const { page, itemsPerPage } = this.options;
      const pageNumber = page;
      let params = {
        limit: itemsPerPage,
        page: pageNumber,
      };
      params = { ...params, ...this.filters }
      getEvents(params).then(
        (data) => {
          this.loading = false;
          this.events = data.results;
          this.totalEvents = data.total;
          this.numberOfPages = data.total / data.limit;
        },
        (error) => {
          this.errorMessage = error;
          console.error('There was an error!', error);
        }
      );
    }
  },
  mounted() {
    this.getEvents();
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
};
</script>
