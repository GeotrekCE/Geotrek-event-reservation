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
            <date-picker label="Date de début" v-model:dateValue="filters.begin_date"
              @input="filters.begin_date = $event">
            </date-picker>
          </v-col>
          <v-col cols="12" lg="6">
            <date-picker label="Date de fin" v-model:dateValue="filters.end_date"
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

<script setup lang="ts">

import { getDistricts, getTouristiceventType } from '@/utils/gta_api';
import DatePicker from './DatePicker.vue';

import { ref, onMounted } from 'vue'
import type { ResaEventFilters } from '@/declaration';

const emits = defineEmits(['search'])

const filters = ref<ResaEventFilters>({
  begin_date: '',
  end_date: '',
  type_id: [],
  massif: []
})
const districts = ref<string[]>([])
const eventtypes = ref<string[]>([])
const filtersState =ref<ResaEventFilters>({
  begin_date: '',
  end_date: '',
  type_id: [],
  massif: []
})// migrate from vuex store

function saveFilters(filters: ResaEventFilters | undefined) {
  console.log('need to be reimplemented (migrate from vuex) ?')
}

function search() {
  saveFilters(filters.value);
  emits('search', filters);
}
function clear() {
  saveFilters(undefined);
  filters.value = filtersState.value;
  emits('search', filters);
}

onMounted(async () => {
  filters.value = filtersState.value;
  const districtsResponse = await getDistricts()
  districts.value = districtsResponse.results.map((item: any) => item.name)
  const eventtypesResponse = await getTouristiceventType()
  eventtypes.value = eventtypesResponse.results.map((item: any) => item.name)
})
</script>

