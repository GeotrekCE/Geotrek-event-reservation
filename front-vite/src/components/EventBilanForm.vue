<template>
  <form @submit.prevent="onSubmit">
  	<div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-10">
      <div class="sm:col-span-2">
        <label for="nb_adultes" class="block text-sm font-medium leading-6 text-gray-900">Adulte(s)</label>
        <div class="mt-2">
          <input
            type="number"
            name="nb_adultes"
            v-model="bilan.nb_adultes"
            id="nb_adultes"
            min="0" 
            class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"
          />
        </div>
      </div>
      <div class="sm:col-span-2">
        <label for="nb_moins_6_ans" class="block text-sm font-medium leading-6 text-gray-900">Moins de 6 ans</label>
        <div class="mt-2">
          <input
            type="number"
            name="nb_moins_6_ans"
            v-model="bilan.nb_moins_6_ans"
            id="nb_moins_6_ans"
            min="0" 
            class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"
          />
        </div>
      </div>
      <div class="sm:col-span-2">
        <label for="nb_6_8_ans" class="block text-sm font-medium leading-6 text-gray-900">6 - 8 ans</label>
        <div class="mt-2">
          <input
            type="number"
            name="nb_6_8_ans"
            v-model="bilan.nb_6_8_ans"
            id="nb_6_8_ans"
            min="0" 
            class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"
          />
        </div>
      </div>
      <div class="sm:col-span-2">
        <label for="nb_9_12_ans" class="block text-sm font-medium leading-6 text-gray-900">9 - 12 ans</label>
        <div class="mt-2">
          <input
            type="number"
            name="nb_9_12_ans"
            v-model="bilan.nb_9_12_ans"
            id="nb_9_12_ans"
            min="0" 
            class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"
          />
        </div>
      </div>
      <div class="sm:col-span-2">
        <label for="nb_plus_12_ans" class="block text-sm font-medium leading-6 text-gray-900">Plus de 12 ans</label>
        <div class="mt-2">
          <input
            type="number"
            name="nb_plus_12_ans"
            v-model="bilan.nb_plus_12_ans"
            id="nb_plus_12_ans"
            min="0" 
            class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"
          />
        </div>
      </div>
      <div class="col-span-full">
        <button
          class="block mx-auto rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm bg-sky-600 hover:bg-sky-500"
          @click.prevent="onPrefillSummary"
        >
          Pré remplir le nombre d'inscrits
        </button>
      </div>
      <div class="col-span-full">
        <label for="commentaire" class="block text-sm font-medium leading-6 text-gray-900">Commentaire</label>
        <div class="mt-2">
          <textarea
            id="commentaire"
            name="commentaire"
            v-model="bilan.commentaire"
            rows="3"
            as="textarea"
            class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"
          />
        </div>
      </div>


    </div>
    <div class="my-6 flex flex-col items-end gap-x-6">
      <button
        type="submit"
        class="rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm"
        :class="{
          'bg-sky-600': !saving,
          'hover:bg-sky-500': !saving,
          'bg-sky-100': saving,
          'hover:bg-sky-100': saving,
          'text-black': saving,
        }"
        :disabled="saving"
      >
        {{ saving ? 'Enregistrement en cours...' : 'Enregistrer bilan' }}
      </button>

      <div v-if="error" class="text-red-500">
        Une erreur est survenue :
        <p>{{ error }}</p>
      </div>

    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { ResaBilan, ResaEvent } from '@/declaration';

const props = defineProps<{
  saving: boolean, 
  originalData: Partial<ResaBilan>,
  error?: string,
  summary?: Partial<ResaEvent>
}>()
const emits = defineEmits(['submit'])

const bilan = ref<any>({
  commentaire: '',
  nb_adultes: 0,
  nb_moins_6_ans: 0,
  nb_6_8_ans: 0,
  nb_9_12_ans: 0,
  nb_plus_12_ans: 0,
  ...props.originalData
})

function onSubmit() {
  emits('submit', bilan.value)
}

function onPrefillSummary() {
  if (!props.summary) return
  bilan.value.nb_adultes = props.summary?.sum_participants_adultes
  bilan.value.nb_moins_6_ans = props.summary?.sum_participants_moins_6_ans
  bilan.value.nb_6_8_ans = props.summary?.sum_participants_6_8_ans
  bilan.value.nb_9_12_ans = props.summary?.sum_participants_9_12_ans
  bilan.value.nb_plus_12_ans = props.summary?.sum_participants_plus_12_ans
}

</script>