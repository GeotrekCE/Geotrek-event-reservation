<template>
  <v-container name="login">
      <v-card class="mb-10" elevation="2">
        <v-card-title>Login</v-card-title>
         <v-form  class="pa-md-4 mx-lg-auto"
          ref="form"
          lazy-validation
        >
          <v-text-field
            v-model="identifiant"
            label="identifiant"
            required
          ></v-text-field>

           <v-text-field
            v-model="password"
            label="password"
            :append-icon="showpass ? 'mdi-eye' : 'mdi-eye-off'"
            required
            :type="showpass ? 'text' : 'password'"
            name="input-password"
            @click:append="showpass = !showpass"
          ></v-text-field>

          <v-btn
            :disabled="!valid"
            color="success"
            class="mr-4"
            @click="login"
          >
            Login
          </v-btn>

        </v-form>
      </v-card>
  </v-container>

</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { config } from '@/config/config'
import { postLogin, postOneReservation } from '@/services/appli_api'

export default {
  components: {},
  data() {
    return {
      identifiant: '',
      password: '',
      showpass: false,
      loginMessage: 'Success',
      openSnackbar: false
    }
  },
  computed: {
    ...mapGetters(['redirectOnLogin']),

    valid() {
      return (this.identifiant !== '' && this.password !== '');
    },
  },
  methods: {
    ...mapActions(['saveUserData', 'snackbarSaveInfo']),

    logout() {
      this.saveUserData({});
    },
    login() {
      const userData = {
        login: this.identifiant,
        password: this.password,
        id_application: config.ID_APPLICATION,
      };

      postLogin(userData).then((data) => {
        const user = { ...data.user, expires: data.expires };
        this.saveUserData(user);
        if (this.redirectOnLogin !== undefined) {
          this.$router.push({ path: this.redirectOnLogin });
        } else {
          this.$router.push({ path: '/' });
        }
      });
    },
  },
  created() {
    this.logout();
  },
  mounted() {

  }
}
</script>
