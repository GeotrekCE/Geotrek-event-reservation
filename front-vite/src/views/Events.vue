<template>
  <div name="event-detail">
    
    <v-container>
      <events-filters @search="() => {getEvents()}" />
    </v-container>

    <table>
      <tr v-for="event in events" :key="event.id">
        <td>
          {{ event }}
        </td>
      </tr>
    </table>

    <!-- <v-data-table
      :page="page"
      :pageCount="numberOfPages"
      :headers="headers"
      :items="events"
      :item-class="row_classes"
      v-model:options="options"
      :server-items-length="totalEvents"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.id="{ item }">
        <router-link :to="{ name: 'event', params: { id: item.id }}">
          <v-btn icon color="blue">
            <v-icon v-if="(item.bilan || {}).annulation">mdi-text-box-remove</v-icon>
            <v-icon v-else>mdi-text-box</v-icon>
          </v-btn>
        </router-link>
      </template>
      <template v-slot:item.name="{ item }">
        <router-link :to="{ name: 'event', params: { id: item.id }}">
          {{ item.name }}
        </router-link>
      </template>
      <template v-slot:item.remplissage="{ item }">
        <reservation-progress :reservation-nb="item.sum_participants"
          :participant-nb="item.capacity"
          :attente-nb="item.sum_participants_liste_attente">
        </reservation-progress>
      </template>
      <template v-slot:item.published="{ item }">
        <v-simple-checkbox v-model="item.published" disabled></v-simple-checkbox>
      </template>
    </v-data-table> -->
  </div>
</template>

<script lang="ts">
import { getEvents } from '@/utils/appli_api';
// import ReservationProgress from '@/components/ReservationProgress.vue';
import EventsFilters from '@/components/EventsFilters.vue';
import { useEventStore } from '@/stores/events'
// import { VDataTable } from 'vuetify/labs/VDataTable'

const eventStore = useEventStore()

export default {
  components: { 
    // ReservationProgress,
    EventsFilters,
    // VDataTable
  },
  name: 'DatatableComponent',
  data() {
    return {
      page: 1,
      totalEvents: 0,
      numberOfPages: 0,
      events: [] as {id: string}[],
      loading: true,
      options: {
        sortBy: ['begin_date'],
        sortDesc: [false],
        page: 0,
        itemsPerPage: 10
      },
      headers: [
        { text: 'Détail', value: 'id', sortable: false },
        { text: 'Nom', value: 'name' },
        { text: 'Publié', value: 'published' },
        { text: 'Remplissage', value: 'remplissage', sortable: false },
        { text: 'Date début', value: 'begin_date' },
        { text: 'Date fin', value: 'end_date' },
        { text: 'Type', value: 'type.type' },
        { text: 'Massif', value: 'massif' },
      ],
      errorMessage: null
    };
  },
  watch: {
    options: {
      handler() {
        this.getEvents();
      },
      deep: true,
    },
  },
  methods: {
    row_classes(item: any) {
      if ((item.bilan || {}).annulation) {
        return 'red lighten-3';
      }
    },
    search() {
      this.options.page = 1;
      this.getEvents();
    },
    getEvents() {
      this.loading = true;
      const {
        page, itemsPerPage, sortBy, sortDesc
      } = this.options;
      let params = {
        limit: itemsPerPage,
        page,
        sortBy,
        sortDesc
      };
      params = { ...params, ...eventStore.filters }
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

<style>
#red {
  background-color: aquamarine;
}
</style>
