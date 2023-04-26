import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import App from './App.vue'
import { router } from './router'

import Router from 'vue-router'
import { store } from '@/store/store'
// import { sync } from 'vuex-router-sync'
import ApiService from '@/services/api_service'
import VueI18n from 'vue-i18n'
import { messages } from '@/i18n/messages'
import { dateTimeFormats } from '@/i18n/datetimeformat'
import VeeValidate from 'vee-validate'
import VueCookies from 'vue-cookies'
import VueSSE from 'vue-sse'
import DatePicker from 'vue2-datepicker'
import 'vue2-datepicker/index.css'
import vuetify from '@/plugins/vuetify'

import { createPinia, PiniaVuePlugin } from 'pinia'
import { authStore } from './stores/AuthStore'

Vue.config.productionTip = false

Vue.use(require('vue-cookies'))
Vue.use(VueCookies)
Vue.use(VueSSE)
Vue.use(DatePicker)

Vue.use(VueI18n)

const i18n = new VueI18n({
  locale:
    typeof process.env.VUE_APP_TARANIS_NG_LOCALE === 'undefined'
      ? 'en'
      : process.env.VUE_APP_TARANIS_NG_LOCALE,
  fallbackLocale: 'en',
  messages,
  dateTimeFormats
})

Vue.use(VeeValidate, {
  i18nRootKey: 'validations',
  i18n
})

const coreAPIURL =
  typeof process.env.VUE_APP_TARANIS_NG_CORE_API === 'undefined'
    ? '/api'
    : process.env.VUE_APP_TARANIS_NG_CORE_API

ApiService.init(coreAPIURL)

// pinia
Vue.use(PiniaVuePlugin)
const pinia = createPinia()

Vue.use(Router)

export const vm = new Vue({
  i18n,
  vuetify,
  pinia,
  store,
  router,
  render: (h) => h(App),
  setup() {
    if (localStorage.ACCESS_TOKEN) {
      const authstore = authStore()
      authstore.setToken(localStorage.ACCESS_TOKEN)
    }
  }
}).$mount('#app')
