<template>
  <div name="event-detail">
    <h1 style="text-align: center;">Animations du Parc national des Cévennes</h1>
    <v-container>
      <events-filters @search="(newAddress) => {getEvents()}"/>
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
          <v-btn icon color="blue" >
            <v-icon>mdi-text-box-multiple</v-icon>
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
          <template v-slot:item.published="{ item }">
        <v-simple-checkbox
          v-model="item.published"
          disabled
        ></v-simple-checkbox>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { getEvents } from '@/services/appli_api';
import ReservationProgress from './subcomponents/ReservationProgress.vue';
import EventsFilters from './subcomponents/EventsFilters.vue';

export default {
  components: { ReservationProgress, EventsFilters },
  name: 'DatatableComponent',
  data() {
    return {
      page: 1,
      totalEvents: 0,
      numberOfPages: 0,
      events: [],
      loading: true,
      options: {},
      headers: [
        { text: 'Détail', value: 'id', sortable: false },
        { text: 'Remplissage', value: 'remplissage', sortable: false },
        { text: 'Publié', value: 'published' },
        { text: 'Nom', value: 'name' },
        { text: 'Date début', value: 'begin_date' },
        { text: 'Date fin', value: 'end_date' },
        { text: 'Type', value: 'type.type' },
        { text: 'Massif', value: 'massif' },
      ],
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
    search() {
      this.options.page = 1;
      this.getEvents();
    },
    getEvents() {
      this.loading = true;
      const {
        page, itemsPerPage, sortBy, sortDesc
      } = this.options;
      const pageNumber = page;
      let params = {
        limit: itemsPerPage,
        page: pageNumber,
        sortBy,
        sortDesc
      };
      params = { ...params, ...this.$store.state.events.filters }
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
  },
};
</script>
