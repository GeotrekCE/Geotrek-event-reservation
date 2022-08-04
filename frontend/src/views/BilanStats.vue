<template>
  <v-container name="event-list">
    <h1>Bilan des animations</h1>
    <div>
      <h2>Filtres</h2>
      <v-select :items="listeYear" label="Année" v-model="selectedYear"></v-select>
    </div>
    <div v-if="!loading">
      <h2>Bilan Global </h2>
      <div>Nombre animations total : {{ stats.nb_animations }}</div>
      <div>Nombre animations annulées : {{ stats.nb_annulation }}</div>
      <div>Nombre animations annulées : {{ stats.nb_annulation }}</div>
      <div>Taux de remplissage : {{ stats.taux_remplissage }}</div>
      <div>Taux de remplissage des animations passées: {{ stats.taux_remplissage_passe }}</div>
    </div>
    <div>
      <h2>Télécharger bilan </h2>
      <v-btn color="primary" dark class="ma-2" :href="URL_APPLICATION + '/export/events'"
        target="_blank">
        Exporter
      </v-btn>
    </div>
    <div :v-if="selectedYear">
      <h2>Graphique</h2>
      <bilan-graphs :config="charts.nbAnimations" :filters="{}">
      </bilan-graphs>
      <bilan-graphs :config="charts.nbDayBeforeResa" :filters="{ year: selectedYear }">
      </bilan-graphs>
    </div>
  </v-container>
</template>

<script>
import BilanGraphs from '@/components/BilanGraphs.vue'
import { config } from '@/config/config';
import * as chartsConfig from '@/config/charts.js'
import { getGlobalStats } from '@/services/appli_api.js'

export default {
  components: { BilanGraphs },
  data() {
    return {
      URL_APPLICATION: config.URL_APPLICATION,
      charts: chartsConfig,
      loading: true,
      stats: {},
      listeYear: [],
      selectedYear: undefined
    }
  },
  methods: {
    refreshGlobalStats() {
      getGlobalStats({ year: this.selectedYear }).then(
        (data) => {
          this.loading = false;
          this.stats = data;
        },
        (error) => {
          console.error('There was an error!', error);
        }
      )
    }
  },
  watch: {
    selectedYear(newselectedYear, oldselectedYear) {
      if (newselectedYear !== oldselectedYear) {
        this.refreshGlobalStats()
      }
    }
  },
  created() {
    // generate year series
    // start animation year = 2016
    // TODO change in config
    const beginYear = 2016;
    this.selectedYear = new Date().getFullYear();
    this.listeYear = [
      ...Array(1 + (this.selectedYear - beginYear)).keys()
    ].map((i) => i + beginYear);
  },
  mounted() {
    this.refreshGlobalStats();
  }
}
</script>

<style>
</style>
