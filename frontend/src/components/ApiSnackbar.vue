<template>
  <v-snackbar
      :value="snackbarState"
      :color="snackbarColor"
      timeout="-1"
    >
      {{ snackbarMessage }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="snackbarSwitchShow(false)"
        >
        <v-icon>mdi-window-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
</template>

<script>

import { mapGetters, mapActions } from 'vuex';

export default {
  data: () => ({

  }),
  computed: {
    ...mapGetters(['snackbarMessage', 'snackbarColor', 'snackbarShow']),

    snackbarState: {
      get() {
        return this.$store.state.snackbar.show;
      },
      set(v) {
        this.snackbarSwitchShow(v);
      }
    }
  },
  methods: {
    ...mapActions(['snackbarSwitchShow']),
  }
};
</script>

<style>

</style>
