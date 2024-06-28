<template>
  <Menubar :model="items" class="app-header">
    <template #start>
      <router-link to="/" class="-m-1.5 p-1.5 flex items-center">
        <img class="h-8 w-auto pr-1.5" src="/assets/logo.svg" alt="">
        <span class=" font-small text-gray-900 m-2">{{ config.TITLE }}</span>
      </router-link>
    </template>
    <template #item="{ item, props, hasSubmenu }">
      <div v-if="isAdmin == item.isAdmin && isAuth == item.isAuth">
        <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
          <a :href="href" v-bind="props.action" @click="navigate"
            :class="item.route == $route.fullPath ? 'p-menuitem-active' : ' '">
            <span :class="item.icon" />
            <span class="ml-2 item-label">{{ item.label }}</span>
          </a>
        </router-link>
      </div>
    </template>
    <template #end>
      <router-link @click="isMenuOpened = false" :to="isAuth ? '/logout' : '/login'"
        class="-mx-3 block rounded-lg px-3 py-2.5 text-base font-medium leading-7 text-gray-900 hover:bg-gray-50">
        {{ isAuth ? 'Déconnexion (' + user?.email + ')' : 'Connexion' }}
      </router-link>
    </template>
  </Menubar>


  <main class="flex-grow">
    <router-view />
  </main>

  <p-confirm-popup />

</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import PConfirmPopup from 'primevue/confirmpopup'

import Menubar from 'primevue/menubar';
const authStore = useAuthStore()

const { isAuth, isAdmin, user } = storeToRefs(authStore)

const isMenuOpened = ref(false)

const config = ref(CONFIGURATION)

const items = ref([
  {
    label: 'Animations',
    icon: 'pi pi-calendar',
    isAuth: true,
    isAdmin: true,
    route: '/events',
    active: false
  },
  {
    label: 'Informations',
    icon: 'pi pi-link',
    isAuth: true,
    isAdmin: true,
    route: '/info_admin'
  },
  {
    label: 'Statistiques',
    icon: 'pi pi-chart-line',
    isAuth: true,
    isAdmin: true,
    route: '/stats'
  },
  {
    label: 'Mes réservations',
    icon: 'pi pi-calendar',
    isAuth: true,
    isAdmin: false,
    route: '/resalisting'
  },
]);
</script>
