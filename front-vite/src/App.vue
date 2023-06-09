<template>
  <header class="bg-sky-500">
    <nav class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
      <div class="flex lg:flex-1">
        <router-link to="/" class="-m-1.5 p-1.5 flex items-center">
          <img class="h-8 w-auto pr-1.5" src="/assets/logo.svg" alt="">
          <span class="text-lg font-semibold leading-6 text-gray-900">Réservation animations</span>
        </router-link>
      </div>
      <div class="flex lg:hidden">
        <button type="button" class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700" @click="isMenuOpened = true">
          <span class="sr-only">Open main menu</span>
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
        </button>
      </div>
      <div class="hidden lg:flex lg:gap-x-12">
        <router-link to="/events" class="text-sm font-semibold leading-6 text-gray-900">Animations</router-link>
        <router-link to="/infos" class="text-sm font-semibold leading-6 text-gray-900">Informations</router-link>
        <router-link to="/stats" class="text-sm font-semibold leading-6 text-gray-900">Statistiques</router-link>
        <router-link to="/resa/1" class="text-sm font-semibold leading-6 text-gray-900">Résa 1</router-link>
        <router-link to="/resaconfirm?token=pouet" class="text-sm font-semibold leading-6 text-gray-900">Confirmation résa</router-link>
      </div>
      <div class="hidden lg:flex lg:flex-1 lg:justify-end">
        <router-link to="/login" class="text-sm font-semibold leading-6 text-gray-900">Connexion<span aria-hidden="true">&rarr;</span></router-link>
      </div>
    </nav>
    <!-- Mobile menu, show/hide based on menu open state. -->
    <div class="lg:hidden" role="dialog" aria-modal="true" v-if="isMenuOpened">
      <!-- Background backdrop, show/hide based on slide-over state. -->
      <div class="fixed inset-0 z-10"></div>
      <div class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
        <div class="flex items-center justify-between">
          <router-link to="/" class="-m-1.5 p-1.5 flex items-center">
            <img class="h-8 w-auto pr-1.5" src="/assets/logo.svg" alt="">
            <span class="text-lg font-semibold leading-6 text-gray-900">Réservation animations</span>
          </router-link>
          <button type="button" class=" rounded-md p-2.5 text-gray-700" @click="isMenuOpened = false">
            <span class="sr-only">Close menu</span>
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="mt-6 flow-root">
          <div class="-my-6 divide-y divide-gray-500/10">
            <div class="space-y-2 py-6">
              <router-link to="/events" class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Animations</router-link>
              <router-link to="/infos" class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Informations</router-link>
              <router-link to="/stats" class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Statistiques</router-link>
            </div>
            <div class="py-6">
              <router-link to="/login" class="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Connexion</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <main>
    <div>
      <router-view/>
    </div>
  </main>
  <!-- v-if="user && user.identifiant" -->
  <!-- <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Animations Logo"
          class="shrink mr-2"
          contain
          src="./assets/logo.svg"
          transition="scale-transition"
          width="40"
        /> </router-link>

        <v-toolbar-title>Reservation animations</v-toolbar-title>
      </div>

      <template
        v-slot:extension
       >
        <v-tabs align-with-title>
          <v-tab to="/">Animations</v-tab>
          <v-tab to="/infos">Informations</v-tab>
          <v-tab to="/stats">Stats</v-tab>
        </v-tabs>
      </template>

      <v-spacer />

      <v-btn
        to="/login"
        text
      >
        <span class="mr-2">{{ user && user.identifiant }}</span>
        <v-icon icon="mdi-open-in-new" />
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>

    <api-snackbar
      v-if="snackbarInfo.show"
      :snackbar-message="snackbarInfo.message"
      :snackbar-color="snackbarInfo.color"
      @close="snackbarInfo.show = false"
    />

  </v-app> -->
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import Menubar from 'primevue/menubar';
import { ref } from 'vue'

const authStore = useAuthStore()
const appStore = useAppStore()

const { user } = storeToRefs(authStore)
const { snackbarInfo } = storeToRefs(appStore)

const isMenuOpened = ref(false)

</script>
