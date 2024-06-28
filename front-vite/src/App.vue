<template>
  <Menubar :model="items" class="app-header">
    <template #start>
      <router-link to="/" class="-m-1.5 p-1.5 flex items-center">
        <img class="h-8 w-auto pr-1.5" src="./assets/logo.svg" alt="" />
        <span class="font-small text-gray-900 m-2">Réservation animations</span>
      </router-link>
    </template>
    <template #item="{ item, props, hasSubmenu }">
      <div v-if="isAdmin == item.isAdmin && isAuth == item.isAuth">
        <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
          <a
            :href="href"
            v-bind="props.action"
            @click="navigate"
            :class="item.route == $route.fullPath ? 'p-menuitem-active' : ' '"
          >
            <span :class="item.icon" />
            <span class="ml-2 item-label">{{ item.label }}</span>
          </a>
        </router-link>
      </div>
      <div v-if="item.href">
        <a :href="item.href" target="_blank">
          <span :class="item.icon" />
          <span class="ml-2">{{ item.label }}</span>
        </a>
      </div>
    </template>
    <template #end>
      <router-link
        @click="isMenuOpened = false"
        :to="isAuth ? '/logout' : '/login'"
        class="-mx-3 block rounded-lg px-3 text-base font-medium leading-7 text-gray-900 hover:bg-gray-50"
      >
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
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { ref, onBeforeMount } from 'vue'
import PConfirmPopup from 'primevue/confirmpopup'
import { getTouristiceventType } from '@/utils/gta_api'
import Menubar from 'primevue/menubar'
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
  }
])

onBeforeMount(async () => {
  // Ajout du menu public 'Évènements'
  // Si la variable DISPLAY_GTR_EVENTS_MENU est activée
  if (config.value.DISPLAY_GTR_EVENTS_MENU === true) {
    // Récupération des types d'évènements sur l'api de GTA
    const eventtypesResponse = await getTouristiceventType()
    const eventtypes_id = eventtypesResponse.results.map((item: any) => [item.id]).join(',')
    items.value.unshift({
      label: 'Évènements',
      icon: 'pi pi-calendar',
      href: config.value.URL_GTR + '/search?event=' + eventtypes_id
    })
  }
})
</script>
