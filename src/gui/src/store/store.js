import { createStore } from 'vuex'

import { authenticator } from '@/store/authenticator.js'
import { assess } from '@/store/assess.js'
import { config } from '@/store/config.js'
import { analyze } from '@/store/analyze.js'
import { publish } from '@/store/publish.js'
import { settings } from '@/store/settings.js'
import { assets } from '@/store/assets.js'
import { dashboard } from '@/store/dashboard.js'
import { users } from '@/store/users.js'
import { filter } from '@/store/filter.js'

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
  coreAPIURL: '/api'
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

  logout(context) {
    context.commit('clearJwtToken')
  },

  setVerticalView(context, data) {
    context.commit('setVerticalView', data)
  },

  setCoreAPIURL(context, url) {
    context.commit('setCoreAPIURL', url)
  }
}

const mutations = {
  setCoreAPIURL(state, url) {
    state.coreAPIURL = url
  },

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

  getSelection(state) {
    return state.selection
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

export const store = createStore({
  state,
  actions,
  mutations,
  getters,
  modules: {
    authenticator,
    assess,
    config,
    analyze,
    publish,
    settings,
    assets,
    dashboard,
    users,
    filter
  }
})
