<template>
  <div class="grid grid-cols-1 sm:grid-cols-6 gap-x-2 gap-y-4 mt-4">

    <div class="col-span-1 sm:col-span-3">
      <label class="block text-sm font-medium leading-6 text-gray-900">
        Événement
      </label>
      <div class="mt-2">
        <div
          class="flex rounded-sm sm:max-w-md"
        >
          <span
            class="block flex-1 border-0 bg-transparent text-gray-600 sm:text-sm sm:leading-6"
          >
            {{ event.name }}
          </span>
        </div>
      </div>
    </div>

    <div class="col-span-1 sm:col-span-3">
      <label class="block text-sm font-medium leading-6 text-gray-900">
        Type
      </label>
      <div class="mt-2">
        <div
          class="flex rounded-sm sm:max-w-md"
        >
          <span
            class="block flex-1 border-0 bg-transparent text-gray-600 sm:text-sm sm:leading-6"
          >
            {{ ( event.type && event.type.type ) || 'Non renseigné' }}
          </span>
        </div>
      </div>
    </div>

    <div class="col-span-1 sm:col-span-3">
      <label class="block text-sm font-medium leading-6 text-gray-900">
        Date de début
      </label>
      <div class="mt-2">
        <div
          class="flex rounded-sm sm:max-w-md"
        >
          <span
            class="block flex-1 border-0 bg-transparent text-gray-600 sm:text-sm sm:leading-6"
          >
            {{ formatDateString(event.begin_date) || 'Non renseigné' }}
          </span>
        </div>
      </div>
    </div>
    <div class="col-span-1 sm:col-span-3">
      <label class="block text-sm font-medium leading-6 text-gray-900">
        Date de fin
      </label>
      <div class="mt-2">
        <div
          class="flex rounded-sm sm:max-w-md"
        >
          <span
            class="block flex-1 border-0 bg-transparent text-gray-600 sm:text-sm sm:leading-6"
          >
            {{ formatDateString(event.end_date) || 'Non renseigné' }}
          </span>
        </div>
      </div>
    </div>
    <div class="col-span-1 sm:col-span-3">
      <label class="block text-sm font-medium leading-6 text-gray-900">
        Capacité
      </label>
      <div class="mt-2">
        <div
          class="flex rounded-sm sm:max-w-md"
        >
          <span
            class="block flex-1 border-0 bg-transparent text-gray-600 sm:text-sm sm:leading-6"
          >
            {{ event.capacity || 'Non renseigné' }}
          </span>
        </div>
      </div>
    </div>

    <div class="col-span-1 sm:col-span-3">
      <label class="block text-sm font-medium leading-6 text-gray-900">
        Massif
      </label>
      <div class="mt-2">
        <div
          class="flex rounded-sm sm:max-w-md"
        >
          <span
            class="block flex-1 border-0 bg-transparent text-gray-600 sm:text-sm sm:leading-6"
          >
            {{ event.massif || 'Non renseigné' }}
          </span>
        </div>
      </div>
    </div>

    <div class="col-span-full">
      <label class="block text-sm font-medium leading-6 text-gray-900">Heure de RDV</label>
      <div class="mt-2 flex-1 overflow-scroll min-h-[4rem] max-h-[10rem] p-2 text-gray-600 sm:text-sm sm:leading-6" v-html="event.start_time" />
    </div>

    <div class="col-span-full">
      <label class="block text-sm font-medium leading-6 text-gray-900">Lieu de RDV</label>
      <div class="mt-2 flex-1 overflow-scroll min-h-[4rem] rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 cursor-not-allowed max-h-[10rem] p-2 text-gray-600 sm:text-sm sm:leading-6" v-html="event.meeting_point" />
    </div>

    <div class="col-span-full">
      <label class="block text-sm font-medium leading-6 text-gray-900">Informations pratiques (fr)</label>
      <div class="mt-2 flex-1 overflow-scroll min-h-[4rem] rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 cursor-not-allowed max-h-[10rem] p-2 text-gray-600 sm:text-sm sm:leading-6" v-html="event.practical_info_fr" />
    </div>

    <div class="col-span-full">
      <label class="block text-sm font-medium leading-6 text-gray-900">Informations pratiques (en)</label>
      <div class="mt-2 flex-1 overflow-scroll min-h-[4rem] rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 cursor-not-allowed max-h-[10rem] p-2 text-gray-600 sm:text-sm sm:leading-6" v-html="event.practical_info_en" />
    </div>

  </div>

  <div
    v-if="event.published === true && gtevent"
    class="grid grid-cols-1 sm:grid-cols-6 gap-x-2 gap-y-4 mt-4"
  >
    <h2 class="col-span-full cursor-pointer" @click="showMore = !showMore">
      <i
        class="w-4 h-4 pi"
        :class="{
          'pi-chevron-down': showMore,
          'pi-chevron-right': !showMore
        }"
      />
      Données GeoTrek
      {{ showMore ? '' : '(Cliquez pour afficher)'}}
    </h2>
    <template v-if="showMore">
      <div
        class="col-span-1 sm:col-span-3"
        v-for="(field, index) in getGtFields(true)"
        :key="index"
      >
        <label class="block text-sm font-medium leading-6 text-gray-900">{{ field.label }} : </label>
        <span v-html="getGtFieldValue(index)"></span>
      </div>
      <div
        class="col-span-1 sm:col-span-3"
        v-for="(field, index) in getGtFields(false)"
        :key="index"
      >
        <label class="block text-sm font-medium leading-6 text-gray-900">{{ field.label }} : </label>
        <span v-html="getGtFieldValue(index)"></span>
      </div>
    </template>
  </div>

</template>

<script setup lang="ts">
import { ref } from 'vue'
import { gtApiFields, type API_FIELDS } from '@/utils/fields'
import { formatDateString } from '@/utils/formatDate'

const props = defineProps({
  event: {
    type: Object,
    required: true,
  },
  gtevent: {
    type: Object,
    required: false
  }
})

const showMore = ref(false)

/**
 * Fonction de gestion des champs geotrek
 */
function getGtFields(main: boolean): API_FIELDS {
  return Object.keys(gtApiFields)
    .filter((key) => gtApiFields[key].main === main)
    .reduce((res, key) => ({ ...res, [key]: gtApiFields[key] }), {});
}

function getGtFieldValue(field: string) {
  return props.gtevent && field.split('.').reduce(
    (subevent, c) => ((c in subevent) ? subevent[c] : subevent),
    props.gtevent
  );
}
</script>