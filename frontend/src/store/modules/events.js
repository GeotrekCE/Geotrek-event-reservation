export default ({
  state: {
    filters: {
      begin_date: undefined,
      end_date: undefined,
      search_name: undefined,
    },
  },
  getters: {},
  mutations: {
    setFilters(state, filters) {
      state.filters = filters;
    },
    resetFilters(state) {
      Object.keys(state.filters).forEach((key) => {
        state.filters[key] = undefined
      });
    }
  },
  actions: {
    saveFilters(context, filters) {
      if (filters === {} || filters === undefined) {
        context.commit('resetFilters')
      } else {
        context.commit('setFilters', filters)
      }
    }
  }
})
