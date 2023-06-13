<template>
  <p-progress-bar
    :value="tauxRemplissage"
    :pt="{ value: { style: { background: colorRemplissage } } }"
  >
    {{ reservationNb }} / {{ participantNb }} + ({{ attenteNb }})
  </p-progress-bar>
</template>

<script setup lang="ts">
import PProgressBar from 'primevue/progressbar';
import { computed } from 'vue';

const props = defineProps(['reservationNb', 'participantNb', 'attenteNb'])

const colorRemplissage = computed(() => {
  const intPraticipantNb = parseInt(props.participantNb, 0);
  if (Number.isNaN(intPraticipantNb)) return 'blue-grey';

  if (props.reservationNb / intPraticipantNb > 1) return 'red';
  if (props.reservationNb / intPraticipantNb > 0.75) return 'lime accent-4';
  if (props.reservationNb / intPraticipantNb > 0.5) return 'lime';
  return 'green';
})

const tauxRemplissage = computed(() => {
  const intPraticipantNb = parseInt(props.participantNb, 0);
  if (Number.isNaN(intPraticipantNb)) return 0;

  return Math.min((props.reservationNb / intPraticipantNb) * 100, 100);
})

</script>
