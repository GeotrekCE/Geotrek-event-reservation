<template>
  <header class="bg-sky-500">
    <nav class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
      <div class="flex lg:flex-1">
        <router-link to="/" class="-m-1.5 p-1.5 flex items-center">
          <img class="h-8 w-auto pr-1.5" src="/assets/logo.svg" alt="">
          <span class="text-2xl font-medium text-gray-900">Réservation animations</span>
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
      <div class="hidden lg:flex lg:gap-x-12" v-if="isAuth">
        <template v-if="isAdmin">
          <router-link to="/events" class="text-sm font-medium leading-6 text-gray-900">Animations (en cours)</router-link>
          <router-link to="/stats" class="text-sm font-medium leading-6 text-gray-900">Statistiques (à migrer)</router-link>  
        </template>
        <template v-else>
          <router-link to="/resalisting" class="text-sm font-medium leading-6 text-gray-900">Mes résas</router-link>
        </template>
        <router-link to="/infos" class="text-sm font-medium leading-6 text-gray-900">Informations</router-link>
      </div>
      <div class="hidden lg:flex lg:flex-1 lg:justify-end">
        <router-link
          :to="isAuth ? '/logout' : '/login'"
          class="text-sm font-medium leading-6 text-gray-900"
        >
          {{ isAuth ? 'Déconnexion (' + user?.email + ')' : 'Connexion' }}
        </router-link>
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
            <span class="text-2xl font-medium text-gray-900">Réservation animations</span>
          </router-link>
          <button type="button" class=" rounded-md p-2.5 text-gray-700" @click="isMenuOpened = false">
            <span class="sr-only">Close menu</span>
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="mt-6 flow-root" v-if="isAuth">
          <div class="-my-6 divide-y divide-gray-500/10">
            <div class="space-y-2 py-6">
              <template v-if="isAdmin">
                <router-link to="/events" class="text-sm font-medium leading-6 text-gray-900">Animations (en cours)</router-link>
                <router-link to="/stats" class="text-sm font-medium leading-6 text-gray-900">Statistiques (à migrer)</router-link>  
              </template>
              <template v-else>
                <router-link to="/resalisting" class="text-sm font-medium leading-6 text-gray-900">Mes résas</router-link>
              </template>
              <router-link to="/infos" class="text-sm font-medium leading-6 text-gray-900">Informations</router-link>
            </div>
            <div class="py-6">
              <router-link
                :to="isAuth ? '/logout' : '/login'"
                class="-mx-3 block rounded-lg px-3 py-2.5 text-base font-medium leading-7 text-gray-900 hover:bg-gray-50"
              >
                {{ isAuth ? 'Déconnexion' : 'Connexion' }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <main>
    <router-view/>
  </main>
  <!--
    <api-snackbar
      v-if="snackbarInfo.show"
      :snackbar-message="snackbarInfo.message"
      :snackbar-color="snackbarInfo.color"
      @close="snackbarInfo.show = false"
    />

  -->
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'
// import { useAppStore } from '@/stores/app'
import { ref } from 'vue'

const authStore = useAuthStore()
// const appStore = useAppStore()

const { isAuth, isAdmin, user } = storeToRefs(authStore)
// const { snackbarInfo } = storeToRefs(appStore)

const isMenuOpened = ref(false)

</script>
