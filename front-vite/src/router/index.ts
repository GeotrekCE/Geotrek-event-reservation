import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth';

import HomeView from '@/views/HomeView.vue'

import LoginView from '@/views/LoginView.vue';
import LoginCallbackView from '@/views/LoginCallbackView.vue';
import LogoutView from '@/views/LogoutView.vue';

// import BilanStats from '@/views/BilanStats.vue';

export const ROUTES_NAMES = {
  HOME: 'HOME',
  LOGIN: 'LOGIN',
  LOGIN_CALLBACK: 'LOGIN_CALLBACK',
  LOGOUT: 'LOGOUT',
  EVENT_LISTING: 'EVENT_LISTING',
  EVENT_DETAIL: 'EVENT_DETAIL',
  STATS: 'STATS',
  RESA_FORM: 'RESA_FORM',
  RESA_LISTING: 'RESA_LISTING',
  RESA_CONFIRM: 'RESA_CONFIRM',
}
export const ROUTES_PATHS = {
  HOME: '/',
  LOGIN: '/login',
  LOGIN_CALLBACK: '/login/callback',
  LOGOUT: '/logout',
  EVENT_LISTING: '/events',
  EVENT_DETAIL: '/events/:id',
  STATS: '/stats',
  RESA_FORM: '/resa/:geotrekid',
  RESA_LISTING: '/resalisting',
  RESA_CONFIRM: '/resaconfirm'
}

const routes = [
  {
    path: ROUTES_PATHS.HOME,
    name: ROUTES_NAMES.HOME,
    component: HomeView,
    meta: {
      requiresAuth: false
    }
  }, {
    path: ROUTES_PATHS.LOGIN,
    name: ROUTES_NAMES.LOGIN,
    component: LoginView,
    meta: {
      requiresAuth: false
    }
  }, { 
    path: ROUTES_PATHS.LOGIN_CALLBACK,
    name: ROUTES_NAMES.LOGIN_CALLBACK,
    component: LoginCallbackView,
    meta: {
      requiresAuth: false
    }
  }, { 
    path: ROUTES_PATHS.LOGOUT,
    name: ROUTES_NAMES.LOGOUT,
    component: LogoutView,
    meta: {
      requiresAuth: true
    }
  }, { 
    path: ROUTES_PATHS.EVENT_LISTING,
    name: ROUTES_NAMES.EVENT_LISTING,
    component: () => import('@/views/EventListingView.vue'),
    meta: { 
      requiresAuth: true 
    },
  }, {
    path: ROUTES_PATHS.EVENT_DETAIL,
    name: ROUTES_NAMES.EVENT_DETAIL,
    component: () => import('@/views/EventListingView.vue'),
    meta: { 
      requiresAuth: true 
    },
  }, {
/*    path: ROUTES_PATHS.STATS,
    name: ROUTES_NAMES.STATS,
    component: BilanStats,
    // meta: { requiresAuth: true },
  }, {*/
    path: ROUTES_PATHS.RESA_FORM,
    name: ROUTES_NAMES.RESA_FORM,
    component: () => import('@/views/ReservationFormView.vue'),
    meta: {
      requiresAuth: false
    }
  }, {
    path: ROUTES_PATHS.RESA_LISTING,
    name: ROUTES_NAMES.RESA_LISTING,
    component: () => import('@/views/ReservationListingView.vue'),
    meta: {
      requiresAuth: true
    }
  }, {
    path: ROUTES_PATHS.RESA_CONFIRM,
    name: ROUTES_NAMES.RESA_CONFIRM,
    component: () => import('@/views/ReservationConfirmationView.vue'),
    meta: {
      requiresAuth: false
    }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  // instead of having to check every route record with
  // to.matched.some(record => record.meta.requiresAuth)
  // if (to.path !== ROUTES_PATHS.LOGIN) {
  //   authStore.redirectOnLogin = to.path
  // }
  if (
    to.name !== ROUTES_NAMES.LOGIN
    && !authStore.isAuth
    && to.meta.requiresAuth
  ) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    next({
      path: ROUTES_PATHS.LOGIN,
      replace: true,
    });
  }
  next();
})

export default router;
