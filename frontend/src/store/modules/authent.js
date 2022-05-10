export default ({
  state: {
    user: {},
    _redirectOnLogin: '/',
  },

  mutations: {
    /**
     * Set user
     */
    setuser(state, userData) {
      state.user = userData;
    },
    redirectOnLogin(state, path) {
      state._redirectOnLogin = path;
    },
  },

  getters: {

    prod: () => !window.webpackHotUpdate,

    redirectOnLogin(state) {
      return state._redirectOnLogin;
    },

    /**
     * Get user
     */
    user(state) {
      return state.user;
    },
    /**
     * Check if user is connected
     */
    isAuth(state) {
      if (!state.user) {
        return false;
      }
      // check date
      // const date = new Date(state.user.expires);
      // const now = new Date();
      return !!(state.user && state.user.id_role);
    },
  },
  actions: {
    saveUserData(context, userData) {
      context.commit('setuser', userData);
    }
  },
})
