export default ({
  state: {
    filters: {
      begin_date: undefined,
      end_date: undefined,
      search_name: undefined,
      'bilan.annulation': undefined,
      published: true,
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
      state.filters.published = true;
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
