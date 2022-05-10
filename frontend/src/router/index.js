import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store';
import EventDetail from '../views/EventDetail.vue';
import Login from '../views/Login.vue';
import Events from '../views/Events.vue';
import Informations from '../views/Informations.vue';
import Bilans from '../views/Bilans.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  }, {
    path: '/',
    name: 'Events',
    component: Events,
    meta: { requiresAuth: true },
  },
  {
    path: '/event/:id',
    name: 'event',
    component: EventDetail,
    meta: { requiresAuth: true },
  }, {
    path: '/infos',
    name: 'informations',
    component: Informations,
    meta: { requiresAuth: true },
  }, {
    path: '/bilans',
    name: 'bilans',
    component: Bilans,
    meta: { requiresAuth: true },
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  // instead of having to check every route record with
  // to.matched.some(record => record.meta.requiresAuth)
  if (to.path !== '/login') {
    store.commit('redirectOnLogin', to.path)
  }
  if ((to.name !== 'Login') && !store.getters.isAuth) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    next({
      path: 'login',
      replace: true,
    });
  }
  next();
})

export default router;
