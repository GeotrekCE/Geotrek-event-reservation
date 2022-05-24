export default ({
  state: {
    message: undefined,
    color: 'success',
    show: false,
  },

  mutations: {
    /**
     * Set user
     */
    setInfo(state, { message, color, show }) {
      state.message = message;
      state.color = color;
      state.show = show;
    },
    switchShow(state, show) {
      state.show = show;
    }
  },

  getters: {
    snackbarMessage(state) {
      return state.message;
    },
    snackbarColor(state) {
      return state.color;
    },
    snackbarShow(state) {
      return state.show || true;
    }
  },
  actions: {
    snackbarSaveInfo(context, data) {
      context.commit('setInfo', data);
    },
    snackbarSwitchShow(context, show) {
      context.commit('switchShow', show);
    }
  },
})
