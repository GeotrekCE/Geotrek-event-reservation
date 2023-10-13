<template>
  <p-progress-bar
    :value="tauxRemplissage"
    :pt="{ value: { style: { background: colorRemplissage } } }"
    class="border border-solid border-gray-500 rounded-sm"
  >
    <span v-if="displayText">{{ reservationNb }} / {{ participantNb }} + ({{ attenteNb }})</span>
    <span v-else>{{ tauxRemplissage }} %</span>
  </p-progress-bar>
</template>

<script setup lang="ts">
import PProgressBar from 'primevue/progressbar';
import { computed } from 'vue';

const props = defineProps({
  reservationNb: {
    type: Number,
    required: true
  },
  participantNb: {
    type: Number,
    required: true,
    default: 0
  },
  attenteNb: {
    type: Number,
    required: true
  },
  displayText: {
    type: Boolean,
    required: false,
    default :true
  }
})

const colorRemplissage = computed(() => {
  if (props.participantNb === 0) return 'blue-grey';

  if (props.reservationNb / props.participantNb > 1) return 'red';
  if (props.reservationNb / props.participantNb > 0.75) return 'lime accent-4';
  if (props.reservationNb / props.participantNb > 0.5) return 'lime';
  return 'green';
})

const tauxRemplissage = computed(() => {
  if (props.participantNb === 0) return 0;

  return Math.min(Math.round(props.reservationNb / props.participantNb * 100), 100);
})

</script>
