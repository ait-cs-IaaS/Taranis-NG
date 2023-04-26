import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
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
  coreAPIURL: process.env.VUE_APP_TARANIS_NG_CORE_API
}

const actions = {
  setUser(context, userData) {
    context.commit('setUser', userData)
  },

  toggleDrawer(context) {
    context.commit('toggleDrawer', !context.state.drawerVisible)
  },

  setDrawer(context, drawerState) {
    context.commit('toggleDrawer', drawerState)
  },

  updateItemCount(context, itemCount) {
    context.commit('updateItemCount', itemCount)
  },

  updateItemCountFiltered(context, filtered) {
    context.commit('updateItemCountFiltered', filtered)
  },

  updateItemCountTotal(context, total) {
    context.commit('updateItemCountTotal', total)
  },

  setVerticalView(context, data) {
    context.commit('setVerticalView', data)
  }
}

const mutations = {
  setUser(state, userData) {
    state.user = userData
  },

  toggleDrawer(state, drawerState) {
    state.drawerVisible = drawerState
  },

  updateItemCount(state, itemCount) {
    state.itemCountFiltered = itemCount.filtered
    state.itemCountTotal = itemCount.total
  },

  updateItemCountFiltered(state, filtered) {
    state.itemCountFiltered = filtered
  },

  updateItemCountTotal(state, total) {
    state.itemCountTotal = total
  },

  setVerticalView(state, data) {
    state.vertical_view = data
    localStorage.setItem('TNGVericalView', data)
  }
}

const getters = {
  getUserId(state) {
    return state.user.id
  },

  getUser(state) {
    return state.user
  },

  getUserName(state) {
    return state.user.name
  },

  getItemCount(state) {
    return { total: state.itemCountTotal, filtered: state.itemCountFiltered }
  },

  getItemCountTotal(state) {
    return state.itemCountTotal
  },

  getItemCountFilterd(state) {
    return state.itemCountFiltered
  },

  getOrganizationName(state) {
    return state.user.organization_name
  },

  getPermissions(state) {
    return state.user.permissions
  },

  getLoadingState(state) {
    return state.loading
  },

  getVerticalView() {
    return state.vertical_view
  },

  getStoreAPIURL() {
    return state.coreAPIURL
  }
}

export const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
})
