import { defineStore } from 'pinia'

export const useMainStore = defineStore('dashboard', {
  state: () => ({
    user: {
      id: '',
      name: '',
      organization_name: '',
      permissions: []
    },
    vertical_view: false,
    itemCountTotal: 0,
    itemCountFiltered: 0,
    drawerVisible: true,
    coreAPIURL: '/api'
  }),
  getters: {
    getItemCount(state) {
      return { total: state.itemCountTotal, filtered: state.itemCountFiltered }
    }
  }
})
