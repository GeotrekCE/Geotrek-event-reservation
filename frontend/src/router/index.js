import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store';
import Ping from '../components/Ping.vue';
import EventDetail from '../components/EventDetail.vue';
import Login from '../components/Login.vue';
import Events from '../components/Events.vue';

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
  },
  {
    path: '/ping',
    name: 'Ping',
    component: Ping,
  },
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
