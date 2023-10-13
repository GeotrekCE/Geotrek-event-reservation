<template>
  <vv-form
    :validation-schema="formSchema"
    :initial-values="formValues"
    as=""
    v-slot="{ values, errors }"
    :validateOnMount="true"
  >
    <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-10">
      <div class="col-span-full">
        <label for="raison_annulation" class="block text-sm font-medium leading-6 text-gray-900">Raison de l'annulation</label>
        <div class="mt-2">
          <vv-field
            id="raison_annulation"
            name="raison_annulation"
            rows="3"
            as="textarea"
            class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"
          />
          <vv-error-message name="raison_annulation" />
        </div>
      </div>

    </div>
    <div class="my-6">
      <button
        class="rounded-sm block mx-auto px-3 py-2 text-sm font-medium text-white shadow-sm disabled:bg-red-100 disabled:text-black disabled:cursor-not-allowed"
        :class="{
          'bg-red-600': !saving,
          'hover:bg-red-500': !saving,
          'bg-red-100': saving,
          'hover:bg-red-100': saving,
          'text-black': saving,
        }"
        :disabled="Object.keys(errors).length > 0 || saving"
        @click="onSubmit($event, values)"
      >
        <i class="pi pi-exclamation-triangle mr-2" />
        <span v-if="annulation">
          {{ saving ? 'Dé annulation en cours...' : 'Dé annuler l\'animation' }}
        </span>
        <span v-else>
          {{ saving ? 'Annulation en cours...' : 'Annuler l\'animation' }}
        </span>

      </button>
      <div v-if="error" class="text-red-500">
        Une erreur est survenue :
        <p>{{ error }}</p>
      </div>
    </div>
  </vv-form>
</template>

<script setup lang="ts">
import { Form as VvForm, Field as VvField, ErrorMessage as VvErrorMessage } from 'vee-validate'
import * as yup from 'yup'

import { useConfirm } from "primevue/useconfirm";

const confirm = useConfirm()

const props = defineProps(['saving', 'annulation', 'raisonAnnulation', 'error'])
const emits = defineEmits(['submit'])

const formValues = {
  raison_annulation: props.raisonAnnulation
}
const formSchema = yup.object().shape({
  raison_annulation: yup.string().required().label('Raison de l\'annulation'),
})
async function onSubmit (event: any, values: any) {
  confirm.require({
    target: event.target,
    message: props.annulation
      ? 'Êtes vous sûr de vouloir dé-annuler cette animation ?'
      : 'Êtes vous sûr de vouloir annuler cette animation ?',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Oui',
    rejectLabel: 'Non',
    async accept () {
      emits('submit', {
        annulation: !props.annulation,
        ...values
      })
    },
  })
}

</script>

<style scoped>
span[role='alert'] {
  color: var(--red-500);
}
</style>