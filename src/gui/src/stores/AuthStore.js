import { authenticate, refresh } from '@/api/auth'
import ApiService from '@/services/api_service'
import { Base64 } from 'js-base64'
import { useMainStore } from './MainStore'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('authenticator', {
  state: () => ({
    jwt: '',
    login_uri: '/login',
    logout_uri: '/logout',
    external_login_uri: false,
    external_logout_uri: false,
    user: {},
    sub: '',
    exp: ''
  }),
  getters: {
    isAuthenticated() {
      const exp = new Date(this.exp * 1000)
      const now = new Date()
      return now < exp
    },

    needTokenRefresh() {
      const exp = new Date((this.exp - 300) * 1000)
      const now = new Date()
      return now > exp
    }
  },
  actions: {
    async login(userData) {
      try {
        const response = await authenticate(userData)
        this.setJwtToken(response.data.access_token)
        const store = useMainStore()
        store.user = this.user
      } catch (error) {
        this.clearJwtToken()
        console.log(error)
        return error.toJSON()
      }
    },
    logout() {
      this.clearJwtToken()
    },
    async refresh() {
      try {
        const response = await refresh()
        this.setJwtToken(response.data.access_token)
        const store = useMainStore()
        store.user = this.user
      } catch {
        this.clearJwtToken()
      }
    },
    setToken(access_token) {
      this.setJwtToken(access_token)
      const store = useMainStore()
      store.user = this.user
    },
    setAuthURLs() {
      this.setLoginURL()
      this.setLogoutURL()
    },
    setJwtToken(access_token) {
      localStorage.ACCESS_TOKEN = access_token
      ApiService.setHeader()
      this.jwt = access_token
      const data = JSON.parse(Base64.decode(access_token.split('.')[1]))
      this.user = data.user_claims
      this.sub = data.sub
      this.exp = data.exp
    },
    clearJwtToken() {
      localStorage.ACCESS_TOKEN = ''
      this.jwt = ''
    },
    setLoginURL() {
      if (
        '$VUE_APP_TARANIS_NG_LOGIN_URL' !== '' &&
        '$VUE_APP_TARANIS_NG_LOGIN_URL'[0] !== '$'
      ) {
        this.login_uri = '$VUE_APP_TARANIS_NG_LOGIN_URL'
        this.external_login_uri = true
      }
      if (process.env.VUE_APP_TARANIS_NG_LOGIN_URL) {
        this.login_uri = process.env.VUE_APP_TARANIS_NG_LOGIN_URL
        this.external_login_uri = true
      }
    },
    setLogoutURL() {
      if (
        '$VUE_APP_TARANIS_NG_LOGOUT_URL' !== '' &&
        '$VUE_APP_TARANIS_NG_LOGOUT_URL'[0] !== '$'
      ) {
        this.logout_uri = '$VUE_APP_TARANIS_NG_LOGOUT_URL'
        this.external_logout_uri = true
      } else if (
        typeof process !== 'undefined' &&
        typeof process.env !== 'undefined' &&
        process.env.VUE_APP_TARANIS_NG_LOGOUT_URL != null
      ) {
        this.logout_uri = process.env.VUE_APP_TARANIS_NG_LOGOUT_URL
        this.external_logout_uri = true
      }
    }
  }
})
