import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth';
// import EventDetail from '@/views/EventDetail.vue';
import LoginView from '@/views/LoginView.vue';
// import Events from '@/views/Events.vue';
// import Informations from '@/views/Informations.vue';
// import BilanStats from '@/views/BilanStats.vue';

import ReservationFormView from '@/views/ReservationForm.vue';
const ReservationConfirmationView = () => import('@/views/ReservationConfirmation.vue')

const ROUTES_NAMES = {
  LOGIN: 'LOGIN',
  EVENTS: 'EVENTS',
  EVENT_DETAIL: 'EVENT_DETAIL',
  INFOS: 'INFOS',
  STATS: 'STATS',
  RESA: 'RESA',
  RESA_CONFIRM: 'RESA_CONFIRM',
}
const ROUTES_PATHS = {
  LOGIN: '/login',
  EVENTS: '/events',
  EVENT_DETAIL: '/events/:id',
  INFOS: '/infos',
  STATS: '/stats',
  RESA: '/resa/:geotrekid',
  RESA_CONFIRM: '/resaconfirm'
}

const routes = [
  {
    path: ROUTES_PATHS.LOGIN,
    name: ROUTES_NAMES.LOGIN,
    component: LoginView,
    meta: {
      requiresAuth: false
    }
  }, { 
  /*
  {
    path: ROUTES_PATHS.EVENTS,
    name: ROUTES_NAMES.EVENTS,
    component: Events,
    // meta: { requiresAuth: true },
  },
   {
    path: ROUTES_PATHS.EVENT_DETAIL,
    name: ROUTES_NAMES.EVENT_DETAIL,
    component: EventDetail,
    // meta: { requiresAuth: true },
  }, {
    path: ROUTES_PATHS.INFOS,
    name: ROUTES_NAMES.INFOS,
    component: Informations,
    // meta: { requiresAuth: true },
  }, {
    path: ROUTES_PATHS.STATS,
    name: ROUTES_NAMES.STATS,
    component: BilanStats,
    // meta: { requiresAuth: true },
  }, {*/
    path: ROUTES_PATHS.RESA,
    name: ROUTES_NAMES.RESA,
    component: ReservationFormView,
    meta: {
      requiresAuth: false
    }
  }, {
    path: ROUTES_PATHS.RESA_CONFIRM,
    name: ROUTES_NAMES.RESA_CONFIRM,
    component: ReservationConfirmationView,
    meta: {
      requiresAuth: false
    }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
//   // instead of having to check every route record with
//   // to.matched.some(record => record.meta.requiresAuth)
//   if (to.path !== ROUTES_PATHS.LOGIN) {
//     authStore.redirectOnLogin = to.path
//   }
//   if ((to.name !== ROUTES_NAMES.LOGIN) && !authStore.isAuth) {
//     // this route requires auth, check if logged in
//     // if not, redirect to login page.
//     next({
//       path: ROUTES_PATHS.LOGIN,
//       replace: true,
//     });
//   }
//   next();
// })

export default router;
