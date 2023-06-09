<template>
  <v-container name="login">
    <v-card class="mb-10" elevation="2">
      <v-card-title>Login</v-card-title>
      <v-form  class="pa-md-4 mx-lg-auto"
        ref="form"
        lazy-validation
      >
        <v-text-field
          v-model="username"
          label="Identifiant"
          required
        />

         <v-text-field
          v-model="password"
          label="Mot de passe"
          :append-icon="showpass ? 'mdi-eye' : 'mdi-eye-off'"
          required
          :type="showpass ? 'text' : 'password'"
          name="input-password"
          @click:append="showpass = !showpass"
        />

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

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const showpass = ref(false)

const valid = computed(() => (username.value !== '' && password.value !== ''))

const authStore = useAuthStore()
function login() {
  authStore.login(username.value, password.value)
}

/**
 * We first logout the user ? (retrieve from the original source code)
 */
authStore.logout()

</script>
