<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <router-link to="/">
        <v-img
          alt="Animations Logo"
          class="shrink mr-2"
          contain
          :src="require('./assets/logo.svg')"
          transition="scale-transition"
          width="40"
        /> </router-link>

      <v-toolbar-title>Reservation animations</v-toolbar-title>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        to="/login"
        text
      >
        <span class="mr-2">{{ user.identifiant }}</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({

  }),
  computed: {
    user() {
      return this.$store.getters.user
    },
  },
};
</script>
