<template>
  <div class="flex min-h-full flex-col">

    <header class="hidden md:block bg-white shadow">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold tracking-tight text-gray-900">
          Bilan des animations
        </h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <section class="mx-auto">
        <h2 class="col-span-full text-2xl">Filtres</h2>
        <select v-model="selectedYear" class="h-10 px-4">
          <option v-for="year in listeYear" :key="year" :value="year">{{ year }}</option>
        </select>
      </section>

      <section
        class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-10 mx-auto"
        v-if="!loading"
      >
        <h2 class="col-span-full text-2xl">Bilan Global </h2>
        <div class="col-span-1 sm:col-span-2">
          Nombre animations total : {{ stats.nb_animations }}
        </div>
        <div class="col-span-1 sm:col-span-2">
          Nombre animations annulées : {{ stats.nb_annulation }}
        </div>
        <div class="col-span-1 sm:col-span-2">
          Nombre animations annulées : {{ stats.nb_annulation }}
        </div>
        <div class="col-span-1 sm:col-span-2">
          Taux de remplissage : {{ stats.taux_remplissage }}
        </div>
        <div class="col-span-1 sm:col-span-2">
          Taux de remplissage des animations passées: {{ stats.taux_remplissage_passe }}
        </div>
        <div class="col-span-full">
          <h2>Télécharger bilan </h2>
          <a :href="URL_APPLICATION + '/export/events'" target="_blank">
            Exporter
          </a>
        </div>
      </section>
      <section
        class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-2 mx-auto"
        v-if="selectedYear"
      >
        <h2 class="col-span-full text-2xl">Graphique</h2>
        <bilan-graphs
          class="col-span-1"
          :config="charts.nbAnimations"
          :filters="{}"
        />
        <bilan-graphs
          class="col-span-1 p-4"
          :config="charts.nbDayBeforeResa"
          :filters="{ year: selectedYear }"
        />
      </section>
    </main>
  </div>
</template>

<script lang="ts">
import BilanGraphs from '@/components/BilanGraphs.vue'
import * as chartsConfig from '@/config/charts'
import { getGlobalStats } from '@/utils/appli_api'
import { type Statistics } from '@/declaration'

export default {
  components: { BilanGraphs },
  data() {
    // generate year series
    // start animation year = 2016
    // TODO change in config
    const beginYear = 2016
    const selectedYear = new Date().getFullYear()
    return {
      URL_APPLICATION: CONFIGURATION.URL_APPLICATION,
      charts: chartsConfig,
      loading: true,
      stats: {} as Statistics,
      listeYear: [
        ...Array(1 + (selectedYear - beginYear)).keys()
      ].map((i) => i + beginYear),
      selectedYear
    }
  },
  methods: {
    async refreshGlobalStats() {
      this.loading = true
      this.stats = await getGlobalStats({ year: this.selectedYear })
      this.loading = false;
    }
  },
  mounted() {
    this.refreshGlobalStats();
  },
  watch: {
    selectedYear(newselectedYear, oldselectedYear) {
      if (newselectedYear !== oldselectedYear) {
        this.refreshGlobalStats()
      }
    }
  }
}
</script>