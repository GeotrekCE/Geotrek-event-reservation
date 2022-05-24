<template>
  <v-progress-linear
      :value="tauxRemplissage"
      :color="colorRemplissage"
      height="25"
      style="min-width: 60px;"
    >{{ reservationNb }} / {{ participantNb }} + ({{ attenteNb }})
    </v-progress-linear>
</template>

<script>
export default {
  props: ['reservationNb', 'participantNb', 'attenteNb'],
  computed: {
    colorRemplissage() {
      const intPraticipantNb = parseInt(this.participantNb, 0);
      if (Number.isNaN(intPraticipantNb)) return 'blue-grey';

      if (this.reservationNb / intPraticipantNb > 1) return 'red';
      if (this.reservationNb / intPraticipantNb > 0.75) return 'lime accent-4';
      if (this.reservationNb / intPraticipantNb > 0.5) return 'lime';
      return 'green';
    },
    tauxRemplissage() {
      const intPraticipantNb = parseInt(this.participantNb, 0);
      if (Number.isNaN(intPraticipantNb)) return 0;

      return (this.reservationNb / intPraticipantNb) * 100;
    }
  }
}
</script>

<style>

</style>
