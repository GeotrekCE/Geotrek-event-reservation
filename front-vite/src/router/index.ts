import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth';

import HomeView from '@/views/HomeView.vue'

import LoginView from '@/views/LoginView.vue';
import LoginCallbackView from '@/views/LoginCallbackView.vue';
import LogoutView from '@/views/LogoutView.vue';
import InfoAdminView from '@/views/InfoAdminView.vue';


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
  INFO_ADMIN: 'INFO_ADMIN'
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
  RESA_CONFIRM: '/resaconfirm',
  INFO_ADMIN: '/info_admin'
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
      requiresAuth: true,
      requiresAdmin: true
    },
  }, {
    path: ROUTES_PATHS.EVENT_DETAIL,
    name: ROUTES_NAMES.EVENT_DETAIL,
    component: () => import('@/views/EventListingView.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    },
  }, {
    path: ROUTES_PATHS.STATS,
    name: ROUTES_NAMES.STATS,
    component: () => import('@/views/StatsView.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    },
  }, {
    path: ROUTES_PATHS.RESA_FORM,
    name: ROUTES_NAMES.RESA_FORM,
    component: () => import('@/views/ReservationFormView.vue'),
    meta: {
      requiresAuth: true
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
  }, {
    path: ROUTES_PATHS.INFO_ADMIN,
    name: ROUTES_NAMES.INFO_ADMIN,
    component: InfoAdminView,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // if we want to display login page
  if (to.name===ROUTES_NAMES.LOGIN) {
    // but user is already auth
    if (authStore.isAuth) {
      // we go to event listing if user is admin
      if (authStore.isAdmin) {
        next({
          path: ROUTES_PATHS.EVENT_LISTING,
          replace: true
        })
      } else {
        // we go to resa listing if user is not admin
        next({
          path: ROUTES_PATHS.RESA_LISTING,
          replace: true
        })
      }
    }
  } else {
    // we are going to a route that may require auth
    if (to.meta.requiresAuth) {
      // if user is not auth, go to login
      if (!authStore.isAuth) {
        if (to.name===ROUTES_NAMES.RESA_FORM) {
          next({
            path: ROUTES_PATHS.HOME,
            replace: true,
        });
        } else {
          next({
            path: ROUTES_PATHS.LOGIN,
            replace: true,
          });
        }
      } else if (
        to.meta.requiresAdmin &&
        !authStore.isAdmin
      ){
        // if the route need admin permission
        // but user is not an admin
        // go to home page
        next({
          path: ROUTES_PATHS.HOME,
          replace: true,
        });
      }

    }
  }
  next();

})

export default router;
