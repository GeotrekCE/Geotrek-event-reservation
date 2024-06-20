<template>
  <div class="flex min-h-full flex-col">

    <header class="hidden md:block bg-white shadow">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold tracking-tight text-gray-900">
          Bilan des animations
        </h1>
      </div>
    </header>

    <main class="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8">
      <section class="mx-auto">
        <h2 class="col-span-full text-2xl">Filtres</h2>
        <select v-model="selectedYear" class="h-10 px-4">
          <option
            v-for="year in listeYear"
            :key="year"
            :value="year"
          >{{ year }}</option>
        </select>

        <div v-if="errorStats" class="text-red-500">
          Une erreur est survenue :
          <p>{{ errorStats }}</p>
        </div>

      </section>


      <section
        class="mt-10"
        v-if="!loading"
      >
        <h2 class="col-span-full text-2xl">Bilan Global </h2> 
        <ul class="list-disc ml-10">
          <li>
            Nombre animations total : {{ stats.nb_animations }}
          </li>
          <li>
            Nombre animations annulées : {{ stats.nb_annulation }}
          </li> 
          <li>
            Taux de remplissage : {{ stats.taux_remplissage }}
          </li>
          <li>
            Taux de remplissage des animations passées: {{ stats.taux_remplissage_passe }}
          </li>
        </ul>
        <div class="col-span-full flex flex-col items-center">
          <a
            class="rounded-sm bg-sky-600 px-3 py-1.5 text-sm font-medium leading-6 text-white shadow-sm hover:bg-sky-500 my-4 mx-auto"
            :href="URL_APPLICATION + '/export/events'"
            target="_blank"
          >
            Télécharger le bilan global
          </a>
        </div>
      </section>

      <section v-else>

        Chargement en cours...

      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { getGlobalStats } from '@/utils/appli_api'
import type { Statistics } from '@/declaration'

import { ref, onBeforeMount, watch } from 'vue'

const beginYear = 2016
const selectedYear = ref(new Date().getFullYear())

const URL_APPLICATION = CONFIGURATION.URL_APPLICATION
const loading = ref(false)
const errorStats = ref<string>('')
const stats = ref<Statistics>({}) 
const listeYear = [
  ...Array(1 + (selectedYear.value - beginYear)).keys()
].map((i) => i + beginYear)

async function refreshGlobalStats() {
  loading.value = true
  errorStats.value = ''
  try {
    stats.value = await getGlobalStats({ year: selectedYear.value })
  } catch (error) {
    errorStats.value = error as string
  }
  loading.value = false;
}
onBeforeMount(() => {
  refreshGlobalStats()
})

watch(
  selectedYear,
  (newselectedYear, oldselectedYear) => {
    if (newselectedYear !== oldselectedYear) {
      refreshGlobalStats()
    }
  }
)
</script>