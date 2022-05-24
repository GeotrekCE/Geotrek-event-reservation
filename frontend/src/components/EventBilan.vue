<template>
  <v-container name="event-list">
    <v-card>
      <v-card-title>
          Bilan de l'animation
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="dialogBilan = true">{{ btnTitle }}</v-btn>
      </v-card-title>
      <v-card-text>
        <div v-if="event.bilan">
          <div><strong>Nb adultes</strong> : {{ event.bilan.nb_adultes }}</div>
          <div><strong>Nb moins 6 ans</strong> : {{ event.bilan.nb_moins_6_ans }}</div>
          <div><strong>Nb 6 8 ans</strong> : {{ event.bilan.nb_6_8_ans }}</div>
          <div><strong>Nb 9 12 ans</strong> : {{ event.bilan.nb_9_12_ans }}</div>
          <div><strong>Nb plus 12 ans</strong> : {{ event.bilan.nb_plus_12_ans }}</div>
          <div><strong>Commentaire</strong> : {{ event.bilan.commentaire }}</div>
        </div>
      </v-card-text>
    </v-card>

    <v-dialog v-model="dialogBilan" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">
              TODO
            </v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeModal">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="closeModal">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
  </v-container>
</template>

<script>
export default {
  props: ['event'],
  data() {
    return {
      liste_champs_nb: ['nb_adultes', 'nb_moins_6_ans', 'nb_6_8_ans', 'nb_9_12_ans', 'nb_plus_12_ans'],
      dialogBilan: false,
    }
  },
  computed: {
    btnTitle() {
      if (this.event.bilan) {
        return 'Modifier bilan';
      }
      return 'Saisir bilan';
    }
  },
  methods: {
    closeModal() {
      this.dialogBilan = false;
    }
  }
}
</script>
