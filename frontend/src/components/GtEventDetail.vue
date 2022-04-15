<template>
  <div>
    <div v-if="this.gtevent === undefined">
      L'événement n'est pas publié sur geotrek. Les détails ne sont pas disponibles
    </div>
    <div v-else>A mettre en forme : {{gtevent}}</div>
    {{gtevent}}
  </div>

</template>

<script>

import { getTouristicEventDetail } from '@/services/gta_api';

export default {
  data() {
    return {
      gtevent: { }
    }
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  created() {
    getTouristicEventDetail(this.id).then(
      (data) => {
        this.gtevent = data.results;
      }
    ).catch((error) => {
      this.gtevent = undefined;
    });
  }
}
</script>

<style>

</style>
